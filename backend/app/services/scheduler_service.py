"""
スケジューラーサービス（バックアップ自動作成用）
"""
import logging
from datetime import datetime, time
from typing import Optional
from sqlalchemy.orm import Session
from ..services.backup_service import create_backup

logger = logging.getLogger(__name__)


def should_run_scheduled_backup(db: Session, backup_time: time = time(2, 0)) -> bool:
    """
    スケジュールバックアップを実行すべきかチェック

    Args:
        db: データベースセッション
        backup_time: バックアップ実行時刻（デフォルト: 02:00）

    Returns:
        bool: 実行すべき場合True
    """
    from ..models.backup import Backup as BackupModel
    from sqlalchemy import func, and_

    now = datetime.now()
    current_time = now.time()

    # 今日のバックアップが既に作成されているかチェック
    today_start = datetime.combine(now.date(), time.min)
    today_backup = db.query(BackupModel).filter(
        and_(
            BackupModel.backup_type == "scheduled",
            BackupModel.created_at >= today_start,
            BackupModel.status == "success"
        )
    ).first()

    # 既に今日のバックアップが存在する場合は実行しない
    if today_backup:
        return False

    # 指定時刻を過ぎている場合のみ実行
    if current_time >= backup_time:
        return True

    return False


def run_scheduled_backup(db: Session) -> Optional[str]:
    """
    スケジュールバックアップを実行

    Args:
        db: データベースセッション

    Returns:
        Optional[str]: バックアップ名（成功時）、None（失敗時）
    """
    try:
        backup_record, backup_path = create_backup(
            db=db,
            backup_name=None,  # 自動生成
            backup_type="scheduled",
            created_by=None,  # システム実行
        )
        logger.info(f"スケジュールバックアップが作成されました: {backup_record.backup_name}")
        return backup_record.backup_name
    except Exception as e:
        logger.error(f"スケジュールバックアップの作成に失敗しました: {str(e)}")
        return None


def cleanup_old_scheduled_backups(db: Session, keep_days: int = 30) -> int:
    """
    古いスケジュールバックアップを削除（保持期間を過ぎたもののみ）

    Args:
        db: データベースセッション
        keep_days: 保持日数

    Returns:
        int: 削除されたバックアップ数
    """
    from datetime import timedelta
    from pathlib import Path
    from ..models.backup import Backup as BackupModel

    cutoff_date = datetime.now() - timedelta(days=keep_days)

    # 古いスケジュールバックアップを取得
    old_backups = db.query(BackupModel).filter(
        BackupModel.backup_type == "scheduled",
        BackupModel.created_at < cutoff_date
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








