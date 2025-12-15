"""
バックアップサービス
"""
import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from ..models.backup import Backup as BackupModel
from ..core.config import settings


BACKUP_DIR = Path("backups")
BACKUP_DIR.mkdir(exist_ok=True)


def get_database_path() -> str:
    """
    データベースファイルのパスを取得

    Returns:
        データベースファイルのパス
    """
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite:///"):
        return db_url.replace("sqlite:///", "")
    return "trade_dx.db"


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
    db_path = get_database_path()

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"データベースファイルが見つかりません: {db_path}")

    # バックアップ名を生成
    if not backup_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"

    # バックアップファイルパス
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
        # データベースファイルをコピー
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
        restore_path: 復元先パス（未指定時は現在のデータベースに上書き）

    Returns:
        bool: 復元が成功したか

    Raises:
        FileNotFoundError: バックアップファイルが見つからない場合
    """
    # バックアップレコードを取得
    backup_record = db.query(BackupModel).filter(BackupModel.id == backup_id).first()
    if not backup_record:
        raise ValueError(f"バックアップID {backup_id} が見つかりません")

    backup_path = Path(backup_record.backup_path)
    if not backup_path.exists():
        raise FileNotFoundError(f"バックアップファイルが見つかりません: {backup_path}")

    # 復元処理開始：ステータスを「in_progress」に更新
    original_status = backup_record.status
    backup_record.status = "in_progress"
    db.commit()
    db.refresh(backup_record)

    try:
        # 復元先パス
        if not restore_path:
            restore_path = get_database_path()

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
