"""
バックアップAPIエンドポイント
"""
from typing import Any, Optional
from datetime import timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ...core.deps import get_db, get_current_active_user, get_current_superuser
from ...models.backup import Backup as BackupModel
from ...models.user import User as UserModel
from ...schemas.backup import (
    Backup,
    BackupCreate,
    BackupRestore,
    BackupListResponse,
)

JST = timezone(timedelta(hours=9))


def to_jst(dt):
    """
    変更日時を日本標準時（UTC+9）に変換して返す。
    SQLiteではUTCで保存されるため、naive datetimeはUTCとして扱う。
    """
    if dt is None:
        return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(JST)
from ...services.backup_service import (
    create_backup,
    restore_backup,
    cleanup_old_backups,
)
from ...services.scheduler_service import (
    should_run_scheduled_backup,
    run_scheduled_backup,
    cleanup_old_scheduled_backups,
)

router = APIRouter()


@router.post("/create", response_model=Backup, status_code=status.HTTP_201_CREATED)
async def create_backup_endpoint(
    backup_data: BackupCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    バックアップを作成

    Args:
        backup_data: バックアップ作成データ
        db: データベースセッション
        current_user: 現在のユーザー

    Returns:
        Backup: 作成されたバックアップ

    Raises:
        HTTPException: バックアップ作成に失敗した場合
    """
    try:
        backup_record, backup_path = create_backup(
            db=db,
            backup_name=backup_data.backup_name,
            backup_type=backup_data.backup_type,
            created_by=current_user.id,
        )
        return backup_record
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"バックアップの作成に失敗しました: {str(e)}"
        )


@router.get("", response_model=BackupListResponse)
async def get_backups(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
    page: int = Query(1, ge=1, description="ページ番号"),
    page_size: int = Query(50, ge=1, le=100, description="1ページあたりの件数"),
    backup_type: Optional[str] = Query(None, description="バックアップタイプフィルタ"),
    status: Optional[str] = Query(None, description="ステータスフィルタ"),
    sort_by: Optional[str] = Query("created_at", description="ソート項目"),
    sort_order: Optional[str] = Query("desc", description="ソート順（asc/desc）"),
) -> Any:
    """
    バックアップ一覧を取得（ページネーション、フィルタリング対応）

    Args:
        db: データベースセッション
        current_user: 現在のユーザー
        page: ページ番号
        page_size: 1ページあたりの件数
        backup_type: バックアップタイプフィルタ
        status: ステータスフィルタ
        sort_by: ソート項目
        sort_order: ソート順

    Returns:
        BackupListResponse: バックアップ一覧とページネーション情報
    """
    from sqlalchemy import and_

    # ベースクエリ
    query = db.query(BackupModel)

    # フィルタリング
    filters = []

    if backup_type:
        filters.append(BackupModel.backup_type == backup_type)

    if status:
        filters.append(BackupModel.status == status)

    if filters:
        query = query.filter(and_(*filters))

    # 総件数を取得
    total = query.count()

    # ソート
    sort_column = getattr(BackupModel, sort_by, BackupModel.created_at)
    if sort_order and sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # ページネーション
    offset = (page - 1) * page_size
    backups = query.offset(offset).limit(page_size).all()

    # 総ページ数を計算
    total_pages = (total + page_size - 1) // page_size

    # 作成日時をJSTに変換してレスポンスを作成
    from ...schemas.backup import Backup as BackupSchema
    backup_items = []
    for backup in backups:
        backup_dict = {
            "id": backup.id,
            "backup_name": backup.backup_name,
            "backup_path": backup.backup_path,
            "backup_type": backup.backup_type,
            "file_size": backup.file_size,
            "record_count": backup.record_count,
            "status": backup.status,
            "error_message": backup.error_message,
            "created_by": backup.created_by,
            "created_at": to_jst(backup.created_at),
        }
        backup_items.append(BackupSchema(**backup_dict))

    return BackupListResponse(
        items=backup_items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{backup_id}", response_model=Backup)
async def get_backup(
    backup_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    バックアップ詳細を取得

    Args:
        backup_id: バックアップID
        db: データベースセッション
        current_user: 現在のユーザー

    Returns:
        Backup: バックアップ詳細

    Raises:
        HTTPException: バックアップが見つからない場合
    """
    backup = db.query(BackupModel).filter(BackupModel.id == backup_id).first()

    if not backup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="バックアップが見つかりません"
        )

    # 作成日時をJSTに変換
    from ...schemas.backup import Backup as BackupSchema
    backup_dict = {
        "id": backup.id,
        "backup_name": backup.backup_name,
        "backup_path": backup.backup_path,
        "backup_type": backup.backup_type,
        "file_size": backup.file_size,
        "record_count": backup.record_count,
        "status": backup.status,
        "error_message": backup.error_message,
        "created_by": backup.created_by,
        "created_at": to_jst(backup.created_at),
    }
    return BackupSchema(**backup_dict)


@router.post("/{backup_id}/restore", status_code=status.HTTP_200_OK)
async def restore_backup_endpoint(
    backup_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_superuser),  # 復元はスーパーユーザーのみ
) -> Any:
    """
    バックアップから復元

    Args:
        backup_id: バックアップID
        db: データベースセッション
        current_user: 現在のユーザー（スーパーユーザーのみ）

    Returns:
        dict: 復元結果

    Raises:
        HTTPException: バックアップが見つからない、復元に失敗した場合
    """
    try:
        success = restore_backup(db=db, backup_id=backup_id)
        if success:
            return {
                "message": "バックアップから復元が完了しました",
                "backup_id": backup_id,
                "success": True
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="バックアップの復元に失敗しました"
            )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"バックアップの復元に失敗しました: {str(e)}"
        )


@router.delete("/{backup_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_backup(
    backup_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_superuser),  # 削除はスーパーユーザーのみ
) -> None:
    """
    バックアップを削除

    Args:
        backup_id: バックアップID
        db: データベースセッション
        current_user: 現在のユーザー（スーパーユーザーのみ）

    Raises:
        HTTPException: バックアップが見つからない場合
    """
    from pathlib import Path

    backup = db.query(BackupModel).filter(BackupModel.id == backup_id).first()

    if not backup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="バックアップが見つかりません"
        )

    # バックアップファイルを削除
    backup_path = Path(backup.backup_path)
    if backup_path.exists():
        backup_path.unlink()

    # レコードを削除
    db.delete(backup)
    db.commit()


@router.post("/cleanup", status_code=status.HTTP_200_OK)
async def cleanup_backups(
    days: int = Query(30, ge=1, description="保持日数"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_superuser),  # クリーンアップはスーパーユーザーのみ
) -> Any:
    """
    古いバックアップを削除

    Args:
        days: 保持日数
        db: データベースセッション
        current_user: 現在のユーザー（スーパーユーザーのみ）

    Returns:
        dict: 削除結果
    """
    deleted_count = cleanup_old_backups(db=db, days=days)
    return {
        "message": f"{deleted_count}件のバックアップを削除しました",
        "deleted_count": deleted_count
    }


@router.post("/run-scheduled", status_code=status.HTTP_200_OK)
async def run_scheduled_backup_endpoint(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_superuser),  # スケジュール実行はスーパーユーザーのみ
) -> Any:
    """
    スケジュールバックアップを手動実行（通常は外部スケジューラーから呼び出し）

    Args:
        db: データベースセッション
        current_user: 現在のユーザー（スーパーユーザーのみ）

    Returns:
        dict: 実行結果
    """
    if not should_run_scheduled_backup(db):
        return {
            "message": "スケジュールバックアップは既に今日実行済みです",
            "executed": False
        }

    backup_name = run_scheduled_backup(db)
    if backup_name:
        return {
            "message": f"スケジュールバックアップが作成されました: {backup_name}",
            "executed": True,
            "backup_name": backup_name
        }
    else:
        return {
            "message": "スケジュールバックアップの作成に失敗しました",
            "executed": False
        }
