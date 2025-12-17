"""
バックアップサービス
"""
import os
import shutil
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from ..models.backup import Backup as BackupModel
from ..core.config import settings


# バックアップディレクトリ（絶対パスを使用）
BACKUP_DIR = Path(os.path.abspath("backups"))
BACKUP_DIR.mkdir(exist_ok=True)


def get_database_path() -> str:
    """
    データベースファイルのパスを取得（SQLite用）

    Returns:
        データベースファイルのパス
    """
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite:///"):
        return db_url.replace("sqlite:///", "")
    return None  # PostgreSQLの場合はNoneを返す


def create_backup(
    db: Session,
    backup_name: Optional[str] = None,
    backup_type: str = "manual",
    created_by: Optional[int] = None
) -> Tuple[BackupModel, str]:
    """
    バックアップを作成

    Args:
        db: データベースセッション
        backup_name: バックアップ名（未指定時は自動生成）
        backup_type: バックアップタイプ
        created_by: 作成者ID

    Returns:
        Tuple[BackupModel, str]: バックアップレコードとファイルパス
    """
    db_url = settings.DATABASE_URL
    is_postgresql = "postgresql" in db_url.lower()

    # バックアップ名を生成
    if not backup_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"

    # バックアップファイルパス
    if is_postgresql:
        backup_filename = f"{backup_name}.json"
    else:
        backup_filename = f"{backup_name}.db"
    backup_path = BACKUP_DIR / backup_filename

    # バックアップレコードを作成（in_progress）
    backup_record = BackupModel(
        backup_name=backup_name,
        backup_path=str(backup_path),
        backup_type=backup_type,
        status="in_progress",
        created_by=created_by,
    )
    db.add(backup_record)
    db.commit()
    db.refresh(backup_record)

    try:
        if is_postgresql:
            # PostgreSQLの場合：データをJSON形式でエクスポート
            backup_data = export_postgresql_data(db)

            # JSONファイルに保存
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2, default=str)

            # ファイルサイズを取得
            file_size = os.path.getsize(backup_path)

            # レコード数を取得（casesテーブルから）
            record_count = backup_data.get('tables', {}).get('cases', {}).get('count', 0)
        else:
            # SQLiteの場合：データベースファイルをコピー
            db_path = get_database_path()
            if not db_path or not os.path.exists(db_path):
                raise FileNotFoundError(f"データベースファイルが見つかりません: {db_path}")

            shutil.copy2(db_path, backup_path)

            # ファイルサイズを取得
            file_size = os.path.getsize(backup_path)

            # レコード数を取得
            conn = sqlite3.connect(str(backup_path))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cases")
            record_count = cursor.fetchone()[0]
            conn.close()

        # バックアップレコードを更新
        backup_record.status = "success"
        backup_record.file_size = file_size
        backup_record.record_count = record_count
        db.commit()
        db.refresh(backup_record)

        return backup_record, str(backup_path)

    except Exception as e:
        # エラー時はバックアップレコードを更新
        backup_record.status = "failed"
        backup_record.error_message = str(e)
        db.commit()

        # バックアップファイルを削除（失敗時）
        if backup_path.exists():
            backup_path.unlink()

        raise


def export_postgresql_data(db: Session) -> dict:
    """
    PostgreSQLのデータをJSON形式でエクスポート

    Args:
        db: データベースセッション

    Returns:
        dict: エクスポートされたデータ
    """
    from ..models.case import Case as CaseModel
    from ..models.customer import Customer as CustomerModel
    from ..models.product import Product as ProductModel
    from ..models.user import User as UserModel
    from ..models.change_history import ChangeHistory as ChangeHistoryModel
    from ..models.document import Document as DocumentModel
    from ..models.case_number import CaseNumber as CaseNumberModel

    backup_data = {
        'exported_at': datetime.now().isoformat(),
        'database_type': 'postgresql',
        'tables': {}
    }

    # 各テーブルのデータをエクスポート
    tables_to_export = [
        ('users', UserModel),
        ('customers', CustomerModel),
        ('products', ProductModel),
        ('case_numbers', CaseNumberModel),
        ('cases', CaseModel),
        ('change_history', ChangeHistoryModel),
        ('documents', DocumentModel),
    ]

    for table_name, model in tables_to_export:
        try:
            records = db.query(model).all()
            records_data = []
            for record in records:
                # SQLAlchemyモデルを辞書に変換
                record_dict = {}
                for column in model.__table__.columns:
                    value = getattr(record, column.name)
                    # datetime等の特殊な型を文字列に変換
                    if hasattr(value, 'isoformat'):
                        value = value.isoformat()
                    record_dict[column.name] = value
                records_data.append(record_dict)

            backup_data['tables'][table_name] = {
                'count': len(records_data),
                'data': records_data
            }
        except Exception as e:
            # テーブルが存在しない場合はスキップ
            backup_data['tables'][table_name] = {
                'count': 0,
                'data': [],
                'error': str(e)
            }

    return backup_data


def restore_backup(
    db: Session,
    backup_id: int,
    restore_path: Optional[str] = None
) -> bool:
    """
    バックアップから復元

    Args:
        db: データベースセッション
        backup_id: バックアップID
        restore_path: 復元先パス（未指定時は現在のデータベースに上書き、PostgreSQLの場合は無視）

    Returns:
        bool: 復元が成功したか

    Raises:
        FileNotFoundError: バックアップファイルが見つからない場合
    """
    # バックアップレコードを取得
    backup_record = db.query(BackupModel).filter(BackupModel.id == backup_id).first()
    if not backup_record:
        raise ValueError(f"バックアップID {backup_id} が見つかりません")

    # バックアップファイルパスを解決（相対パスの場合は絶対パスに変換）
    backup_path_str = backup_record.backup_path
    if not os.path.isabs(backup_path_str):
        # 相対パスの場合、BACKUP_DIRからの相対パスとして解決
        backup_path = BACKUP_DIR / backup_path_str
    else:
        backup_path = Path(backup_path_str)
    
    # さらに、backupsディレクトリ内のファイル名のみが指定されている場合
    if not backup_path.exists() and not os.path.isabs(backup_path_str):
        # ファイル名のみの場合
        backup_path = BACKUP_DIR / os.path.basename(backup_path_str)
    
    if not backup_path.exists():
        raise FileNotFoundError(f"バックアップファイルが見つかりません: {backup_path} (元のパス: {backup_record.backup_path})")

    # 復元処理開始：ステータスを「in_progress」に更新
    original_status = backup_record.status
    backup_record.status = "in_progress"
    db.commit()
    db.refresh(backup_record)

    try:
        db_url = settings.DATABASE_URL
        is_postgresql = "postgresql" in db_url.lower()

        if is_postgresql:
            # PostgreSQLの場合：JSONファイルからデータを復元
            # まず現在のデータをバックアップ（安全のため）
            safety_backup_record = None
            try:
                safety_backup_record, safety_backup_path = create_backup(
                    db=db,
                    backup_name=f"safety_backup_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    backup_type="safety",
                    created_by=None
                )
                import logging
                logging.info(f"安全バックアップを作成しました: {safety_backup_path}")
            except Exception as e:
                # 安全バックアップの作成に失敗しても続行（警告のみ）
                import logging
                logging.warning(f"安全バックアップの作成に失敗しました: {str(e)}")
                # 安全バックアップが作成されなかった場合でも復元は続行

            # JSONファイルを読み込んで復元
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)

            import_postgresql_data(db, backup_data)
        else:
            # SQLiteの場合：データベースファイルをコピー
            if not restore_path:
                restore_path = get_database_path()
                if not restore_path:
                    raise ValueError("復元先パスが指定されていません")

            # 現在のデータベースをバックアップ（安全のため）
            current_db_path = Path(restore_path)
            if current_db_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safety_backup_path = BACKUP_DIR / f"safety_backup_before_restore_{timestamp}.db"
                shutil.copy2(current_db_path, safety_backup_path)

            # バックアップファイルを復元先にコピー
            shutil.copy2(backup_path, restore_path)

        # 復元完了：ステータスを元に戻す（または「success」に設定）
        backup_record.status = original_status if original_status == "success" else "success"
        backup_record.error_message = None
        db.commit()
        db.refresh(backup_record)

        return True

    except Exception as e:
        # エラー時はステータスを「failed」に更新
        backup_record.status = "failed"
        backup_record.error_message = f"復元に失敗しました: {str(e)}"
        db.commit()
        db.refresh(backup_record)
        raise


def import_postgresql_data(db: Session, backup_data: dict) -> None:
    """
    PostgreSQLにJSON形式のデータをインポート

    Args:
        db: データベースセッション
        backup_data: インポートするデータ
    """
    from ..models.case import Case as CaseModel
    from ..models.customer import Customer as CustomerModel
    from ..models.product import Product as ProductModel
    from ..models.user import User as UserModel
    from ..models.change_history import ChangeHistory as ChangeHistoryModel
    from ..models.document import Document as DocumentModel
    from ..models.case_number import CaseNumber as CaseNumberModel
    from sqlalchemy import inspect

    # テーブルマッピング
    table_mapping = {
        'users': UserModel,
        'customers': CustomerModel,
        'products': ProductModel,
        'case_numbers': CaseNumberModel,
        'cases': CaseModel,
        'change_history': ChangeHistoryModel,
        'documents': DocumentModel,
    }

    # 外部キー制約を考慮して順序を定義（依存関係の順）
    import_order = ['users', 'customers', 'products', 'case_numbers', 'cases', 'change_history', 'documents']

    try:
        # 既存のデータを削除（注意：本番環境では慎重に）
        # ただし、usersテーブルは最後に削除（セッション維持のため）
        tables_to_delete = [t for t in reversed(import_order) if t != 'users']
        for table_name in tables_to_delete:
            if table_name in table_mapping:
                model = table_mapping[table_name]
                db.query(model).delete()

        # usersテーブルは最後に削除
        if 'users' in table_mapping:
            db.query(table_mapping['users']).delete()

        db.commit()

        # データをインポート
        for table_name in import_order:
            if table_name not in backup_data.get('tables', {}):
                continue

            model = table_mapping.get(table_name)
            if not model:
                continue

            table_data = backup_data['tables'][table_name]
            records_data = table_data.get('data', [])

            for record_data in records_data:
                # 辞書からモデルインスタンスを作成
                # 日付文字列をdatetimeに変換
                processed_data = {}
                for key, value in record_data.items():
                    if isinstance(value, str):
                        try:
                            # ISO形式の日付文字列をdatetimeに変換
                            if 'T' in value or (len(value) >= 19 and len(value) <= 26):
                                from datetime import datetime as dt
                                # ISO形式の文字列をdatetimeに変換
                                if value.endswith('Z'):
                                    value = value[:-1] + '+00:00'
                                try:
                                    processed_data[key] = dt.fromisoformat(value.replace('Z', '+00:00'))
                                except:
                                    processed_data[key] = value
                            else:
                                processed_data[key] = value
                        except:
                            processed_data[key] = value
                    else:
                        processed_data[key] = value

                # IDを含めて復元（既存のIDを保持）
                # ただし、IDがNoneの場合は除外
                if 'id' in processed_data and processed_data['id'] is not None:
                    # 既存のレコードを確認（削除後なので存在しないはず）
                    existing = db.query(model).filter(model.id == processed_data['id']).first()
                    if existing:
                        # 既存のレコードを更新
                        for key, value in processed_data.items():
                            if key != 'id' and hasattr(existing, key):
                                try:
                                    setattr(existing, key, value)
                                except Exception as e:
                                    # 設定に失敗した場合はスキップ（ログに記録）
                                    import logging
                                    logging.warning(f"フィールド {key} の設定に失敗しました: {str(e)}")
                    else:
                        # 新規作成（IDを指定）
                        try:
                            record = model(**processed_data)
                            db.add(record)
                        except Exception as e:
                            # ID指定での作成に失敗した場合、IDを除外して再試行
                            import logging
                            logging.warning(f"ID指定での作成に失敗しました（ID除外して再試行）: {str(e)}")
                            record_data_without_id = {k: v for k, v in processed_data.items() if k != 'id'}
                            record = model(**record_data_without_id)
                            db.add(record)
                else:
                    # IDがない場合は新規作成（IDは自動生成）
                    record_data_without_id = {k: v for k, v in processed_data.items() if k != 'id'}
                    record = model(**record_data_without_id)
                    db.add(record)

        db.commit()

        # PostgreSQLの場合、シーケンスを更新
        db_url = settings.DATABASE_URL
        if "postgresql" in db_url.lower():
            try:
                from sqlalchemy import text
                # 各テーブルのシーケンスを更新
                sequence_updates = [
                    ("users", "users_id_seq"),
                    ("customers", "customers_id_seq"),
                    ("products", "products_id_seq"),
                    ("case_numbers", "case_numbers_id_seq"),
                    ("cases", "cases_id_seq"),
                    ("change_history", "change_history_id_seq"),
                    ("documents", "documents_id_seq"),
                ]

                for table_name, sequence_name in sequence_updates:
                    if table_name in backup_data.get('tables', {}):
                        table_data = backup_data['tables'][table_name]
                        records_data = table_data.get('data', [])
                        if records_data:
                            # 最大IDを取得
                            max_id = max([r.get('id', 0) for r in records_data if r.get('id')], default=0)
                            if max_id > 0:
                                # シーケンスを更新
                                try:
                                    db.execute(text(f"SELECT setval('{sequence_name}', {max_id}, true)"))
                                except Exception as seq_error:
                                    # シーケンスが存在しない場合はスキップ
                                    import logging
                                    logging.warning(f"シーケンス {sequence_name} の更新に失敗しました: {str(seq_error)}")

                db.commit()
            except Exception as seq_update_error:
                import logging
                logging.warning(f"シーケンスの更新中にエラーが発生しました: {str(seq_update_error)}")
                # シーケンス更新の失敗は致命的ではないので続行

    except Exception as e:
        db.rollback()
        raise Exception(f"データのインポートに失敗しました: {str(e)}")


def cleanup_old_backups(db: Session, days: int = 30) -> int:
    """
    古いバックアップを削除

    Args:
        db: データベースセッション
        days: 保持日数（デフォルト30日）

    Returns:
        int: 削除されたバックアップ数
    """
    from datetime import timedelta

    cutoff_date = datetime.now() - timedelta(days=days)

    # 古いバックアップレコードを取得
    old_backups = db.query(BackupModel).filter(
        BackupModel.created_at < cutoff_date,
        BackupModel.backup_type != "scheduled"  # スケジュールバックアップは削除しない
    ).all()

    deleted_count = 0
    for backup in old_backups:
        # ファイルを削除
        backup_path = Path(backup.backup_path)
        if backup_path.exists():
            backup_path.unlink()

        # レコードを削除
        db.delete(backup)
        deleted_count += 1

    db.commit()
    return deleted_count
