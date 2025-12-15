"""
変更履歴APIエンドポイント
"""
from typing import Any, Optional
from datetime import timezone, timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from ...core.deps import get_db, get_current_active_user
from ...models.change_history import ChangeHistory as ChangeHistoryModel
from ...models.case import Case as CaseModel
from ...models.user import User as UserModel
from ...schemas.change_history import (
    ChangeHistory,
    ChangeHistoryListResponse,
    ChangeHistoryListItem
)

router = APIRouter()

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


def resolve_case_number(history: ChangeHistoryModel) -> Optional[str]:
    """
    履歴ごとの案件番号を解決する。
    案件そのものを参照すると最新の番号に置き換わってしまうため、
    changes_json に保存されたスナップショットを優先して利用する。
    """
    case_number = None

    if history.changes_json and isinstance(history.changes_json, dict):
        snapshot = history.changes_json.get("_case_number_snapshot")
        if isinstance(snapshot, str) and snapshot:
            return snapshot

    case_number_data = None
    if history.changes_json and isinstance(history.changes_json, dict):
        case_number_data = history.changes_json.get("case_number")

    if isinstance(case_number_data, dict):
        if history.change_type == "DELETE":
            case_number = case_number_data.get("old") or case_number_data.get("new")
        elif history.change_type == "CREATE":
            case_number = case_number_data.get("new") or case_number_data.get("old")
        else:
            case_number = case_number_data.get("new") or case_number_data.get("old")
    elif isinstance(case_number_data, str):
        case_number = case_number_data

    # 単一フィールド変更時にfield_name/new_valueに入っている場合
    if not case_number and history.field_name == "case_number":
        case_number = history.new_value or history.old_value

    if not case_number:
        case_number = f"ID:{history.case_id}"

    return case_number


@router.get("", response_model=ChangeHistoryListResponse)
async def get_change_history(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
    page: int = Query(1, ge=1, description="ページ番号"),
    page_size: int = Query(50, ge=1, le=100, description="1ページあたりの件数"),
    case_id: Optional[int] = Query(None, description="案件IDフィルタ"),
    case_number: Optional[str] = Query(None, description="案件番号フィルタ（部分一致）"),
    change_type: Optional[str] = Query(None, description="変更タイプフィルタ（CREATE/UPDATE/DELETE）"),
    sort_by: Optional[str] = Query("changed_at", description="ソート項目"),
    sort_order: Optional[str] = Query("desc", description="ソート順（asc/desc）"),
) -> Any:
    """
    変更履歴一覧を取得（ページネーション、フィルタリング対応）

    Args:
        db: データベースセッション
        current_user: 現在のユーザー
        page: ページ番号
        page_size: 1ページあたりの件数
        case_id: 案件IDフィルタ
        change_type: 変更タイプフィルタ
        sort_by: ソート項目
        sort_order: ソート順

    Returns:
        ChangeHistoryListResponse: 変更履歴一覧とページネーション情報
    """
    # ベースクエリ（案件が削除されていても履歴は取得できる）
    query = db.query(ChangeHistoryModel)

    # フィルタリング（案件番号によるフィルタリングは後でPython側で行う）
    filters = []

    if case_id:
        filters.append(ChangeHistoryModel.case_id == case_id)

    if change_type:
        filters.append(ChangeHistoryModel.change_type == change_type)

    if filters:
        query = query.filter(and_(*filters))

    # 案件番号によるフィルタリングまたはソートが必要な場合は、全件取得してPython側で処理
    # それ以外の場合はDBレベルでソート・ページネーション
    need_case_number_processing = case_number or sort_by == "case_number"

    if need_case_number_processing:
        # 全件取得してPython側でフィルタリング・ソート
        all_histories = query.all()

        # 変更者名と案件番号を取得してリスト化
        items_with_case_number = []
        for history in all_histories:
            # 変更者名を取得
            changed_by_name = None
            if history.changed_by:
                user = db.query(UserModel).filter(UserModel.id == history.changed_by).first()
                if user:
                    changed_by_name = user.username

            # 案件番号（履歴時点のスナップショット）を取得
            resolved_case_number = resolve_case_number(history)

            # 案件番号による部分一致フィルタリング
            if case_number and case_number.lower() not in (resolved_case_number or '').lower():
                continue

            item = {
                'history': history,
                'changed_by_name': changed_by_name,
                'case_number': resolved_case_number,
                'changed_at': history.changed_at,
            }
            items_with_case_number.append(item)

        # 案件番号によるソート
        if sort_by == "case_number":
            reverse = sort_order and sort_order.lower() != "asc"
            items_with_case_number.sort(
                key=lambda x: x['case_number'] or '',
                reverse=reverse
            )
        else:
            # その他のソート項目
            if sort_by == "changed_at":
                reverse = sort_order and sort_order.lower() != "asc"
                items_with_case_number.sort(
                    key=lambda x: x['changed_at'] or datetime.min.replace(tzinfo=timezone.utc),
                    reverse=reverse
                )
            elif sort_by == "id":
                reverse = sort_order and sort_order.lower() != "asc"
                items_with_case_number.sort(
                    key=lambda x: x['history'].id,
                    reverse=reverse
                )

        # 総件数
        total = len(items_with_case_number)

        # ページネーション
        offset = (page - 1) * page_size
        paginated_items = items_with_case_number[offset:offset + page_size]

        # レスポンス用にデータを整形
        items = []
        for item_data in paginated_items:
            history = item_data['history']
            item = ChangeHistoryListItem(
                id=history.id,
                case_id=history.case_id,
                case_number=item_data['case_number'],
                changed_by=history.changed_by,
                changed_by_name=item_data['changed_by_name'],
                change_type=history.change_type,
                field_name=history.field_name,
                old_value=history.old_value,
                new_value=history.new_value,
                changes_json=history.changes_json,
                notes=history.notes,
                changed_at=to_jst(history.changed_at),
            )
            items.append(item)
    else:
        # 通常のDBレベルでのソート・ページネーション
        # ソート
        sort_column = getattr(ChangeHistoryModel, sort_by, ChangeHistoryModel.changed_at)
        if sort_order and sort_order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # 総件数を取得
        total = query.count()

        # ページネーション
        offset = (page - 1) * page_size
        histories = query.offset(offset).limit(page_size).all()

        # レスポンス用にデータを整形
        items = []
        for history in histories:
            # 変更者名を取得
            changed_by_name = None
            if history.changed_by:
                user = db.query(UserModel).filter(UserModel.id == history.changed_by).first()
                if user:
                    changed_by_name = user.username

            # 案件番号（履歴時点のスナップショット）を取得
            resolved_case_number = resolve_case_number(history)

            item = ChangeHistoryListItem(
                id=history.id,
                case_id=history.case_id,
                case_number=resolved_case_number,
                changed_by=history.changed_by,
                changed_by_name=changed_by_name,
                change_type=history.change_type,
                field_name=history.field_name,
                old_value=history.old_value,
                new_value=history.new_value,
                changes_json=history.changes_json,
                notes=history.notes,
                changed_at=to_jst(history.changed_at),
            )
            items.append(item)

    # 総ページ数を計算
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    return ChangeHistoryListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{history_id}", response_model=ChangeHistory)
async def get_change_history_detail(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    変更履歴詳細を取得

    Args:
        history_id: 変更履歴ID
        db: データベースセッション
        current_user: 現在のユーザー

    Returns:
        ChangeHistory: 変更履歴詳細

    Raises:
        HTTPException: 変更履歴が見つからない場合
    """
    history = db.query(ChangeHistoryModel).filter(
        ChangeHistoryModel.id == history_id
    ).first()

    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="変更履歴が見つかりません"
        )

    history.changed_at = to_jst(history.changed_at)
    return history


@router.get("/case/{case_id}/history", response_model=ChangeHistoryListResponse)
async def get_case_change_history(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
    page: int = Query(1, ge=1, description="ページ番号"),
    page_size: int = Query(50, ge=1, le=100, description="1ページあたりの件数"),
) -> Any:
    """
    特定案件の変更履歴を取得

    Args:
        case_id: 案件ID
        db: データベースセッション
        current_user: 現在のユーザー
        page: ページ番号
        page_size: 1ページあたりの件数

    Returns:
        ChangeHistoryListResponse: 変更履歴一覧とページネーション情報

    Raises:
        HTTPException: 案件が見つからない場合
    """
    # 案件の存在確認
    case = db.query(CaseModel).filter(CaseModel.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="案件が見つかりません"
        )

    # 変更履歴を取得
    return await get_change_history(
        db=db,
        current_user=current_user,
        page=page,
        page_size=page_size,
        case_id=case_id,
        case_number=None,  # 明示的にNoneを渡す
        change_type=None,  # 明示的にNoneを渡す
        sort_by="changed_at",
        sort_order="desc"
    )
