"""
案件APIエンドポイント
"""
from typing import Any, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_

from ...core.deps import get_db, get_current_active_user
from ...models.case import Case as CaseModel
from ...models.user import User as UserModel
from ...models.customer import Customer as CustomerModel
from ...models.product import Product as ProductModel
from ...schemas.case import (
    Case,
    CaseCreate,
    CaseUpdate,
    CaseListResponse,
    CaseListItem
)
from ...services.change_history_service import record_change_history
from .websocket import notify_case_updated
from copy import deepcopy

router = APIRouter()


@router.get("", response_model=CaseListResponse)
async def get_cases(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
    page: int = Query(1, ge=1, description="ページ番号"),
    page_size: int = Query(50, ge=1, le=100, description="1ページあたりの件数"),
    search: Optional[str] = Query(None, description="検索キーワード（案件番号、顧客名、商品名）"),
    trade_type: Optional[str] = Query(None, description="区分フィルタ"),
    status: Optional[str] = Query(None, description="ステータスフィルタ"),
    pic: Optional[str] = Query(None, description="担当者フィルタ"),
    shipment_date_from: Optional[date] = Query(None, description="船積予定日（開始）"),
    shipment_date_to: Optional[date] = Query(None, description="船積予定日（終了）"),
    sort_by: Optional[str] = Query("created_at", description="ソート項目"),
    sort_order: Optional[str] = Query("desc", description="ソート順（asc/desc）"),
) -> Any:
    """
    案件一覧を取得（ページネーション、フィルタリング、検索対応）

    Args:
        db: データベースセッション
        current_user: 現在のユーザー
        page: ページ番号
        page_size: 1ページあたりの件数
        search: 検索キーワード
        trade_type: 区分フィルタ
        status: ステータスフィルタ
        pic: 担当者フィルタ
        shipment_date_from: 船積予定日（開始）
        shipment_date_to: 船積予定日（終了）
        sort_by: ソート項目
        sort_order: ソート順

    Returns:
        CaseListResponse: 案件一覧とページネーション情報
    """
    # ベースクエリ
    query = db.query(CaseModel).options(
        joinedload(CaseModel.customer),
        joinedload(CaseModel.product)
    )

    # フィルタリング
    filters = []

    if search:
        # 検索キーワードで案件番号、顧客名、商品名を検索
        search_filter = or_(
            CaseModel.case_number.ilike(f"%{search}%"),
            CustomerModel.customer_name.ilike(f"%{search}%"),
            ProductModel.product_name.ilike(f"%{search}%")
        )
        query = query.join(CustomerModel).join(ProductModel)
        filters.append(search_filter)

    if trade_type:
        filters.append(CaseModel.trade_type == trade_type)

    if status:
        filters.append(CaseModel.status == status)

    if pic:
        filters.append(CaseModel.pic.ilike(f"%{pic}%"))

    # 船積予定日のフィルタリング
    if shipment_date_from:
        filters.append(CaseModel.shipment_date >= shipment_date_from)
    if shipment_date_to:
        filters.append(CaseModel.shipment_date <= shipment_date_to)

    if filters:
        query = query.filter(and_(*filters))

    # 総件数を取得
    total = query.count()

    # ソート
    sort_column = getattr(CaseModel, sort_by, CaseModel.created_at)
    if sort_order and sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # ページネーション
    offset = (page - 1) * page_size
    cases = query.offset(offset).limit(page_size).all()

    # 総ページ数を計算
    total_pages = (total + page_size - 1) // page_size

    # レスポンス用にデータを整形
    items = []
    for case in cases:
        item = CaseListItem(
            id=case.id,
            case_number=case.case_number,
            trade_type=case.trade_type,
            customer_id=case.customer_id,
            customer_name=case.customer.customer_name if case.customer else None,
            product_id=case.product_id,
            product_name=case.product.product_name if case.product else None,
            quantity=case.quantity,
            unit=case.unit,
            sales_amount=case.sales_amount,
            gross_profit=case.gross_profit,
            gross_profit_rate=case.gross_profit_rate,
            status=case.status,
            pic=case.pic,
            shipment_date=case.shipment_date,
            created_at=case.created_at,
            updated_at=case.updated_at,
        )
        items.append(item)

    return CaseListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{case_id}", response_model=Case)
async def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    案件詳細を取得

    Args:
        case_id: 案件ID
        db: データベースセッション
        current_user: 現在のユーザー

    Returns:
        Case: 案件詳細

    Raises:
        HTTPException: 案件が見つからない場合
    """
    case = db.query(CaseModel).options(
        joinedload(CaseModel.customer),
        joinedload(CaseModel.product)
    ).filter(CaseModel.id == case_id).first()

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="案件が見つかりません"
        )

    return case


@router.post("", response_model=Case, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_in: CaseCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    新規案件を作成

    Args:
        case_in: 案件作成データ
        db: データベースセッション
        current_user: 現在のユーザー

    Returns:
        Case: 作成された案件

    Raises:
        HTTPException: 顧客または商品が存在しない、案件番号が重複している場合
    """
    # 顧客の存在確認
    customer = db.query(CustomerModel).filter(CustomerModel.id == case_in.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された顧客が見つかりません"
        )

    # 商品の存在確認
    product = db.query(ProductModel).filter(ProductModel.id == case_in.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された商品が見つかりません"
        )

    # 案件番号の重複確認（案件番号が指定されている場合）
    if case_in.case_number:
        existing_case = db.query(CaseModel).filter(
            CaseModel.case_number == case_in.case_number
        ).first()
        if existing_case:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="指定された案件番号は既に使用されています"
            )

    # 案件を作成
    case_data = case_in.model_dump()
    case = CaseModel(**case_data)
    case.created_by = current_user.id
    case.updated_by = current_user.id

    # 金額を計算
    case.calculate_amounts()

    db.add(case)
    db.commit()
    db.refresh(case)

    # 変更履歴を記録
    try:
        record_change_history(
            db=db,
            case_id=case.id,
            change_type="CREATE",
            changed_by=current_user.id,
            new_case=case,
            case_number_snapshot=case.case_number
        )
        db.commit()
    except Exception as e:
        # 変更履歴記録エラーは警告のみ（案件作成は成功）
        import logging
        db.rollback()
        logging.warning(f"変更履歴の記録に失敗しました: {str(e)}")

    # リレーションを読み込んで返す
    case = db.query(CaseModel).options(
        joinedload(CaseModel.customer),
        joinedload(CaseModel.product)
    ).filter(CaseModel.id == case.id).first()

    # WebSocket通知を送信（全ユーザーに送信）
    try:
        await notify_case_updated(case.id, "created", user_id=None)
    except Exception as e:
        import logging
        logging.warning(f"WebSocket通知の送信に失敗しました: {str(e)}")

    return case


@router.put("/{case_id}", response_model=Case)
async def update_case(
    case_id: int,
    case_in: CaseUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    案件を更新

    Args:
        case_id: 案件ID
        case_in: 案件更新データ
        db: データベースセッション
        current_user: 現在のユーザー

    Returns:
        Case: 更新された案件

    Raises:
        HTTPException: 案件が見つからない、顧客または商品が存在しない場合
    """
    # 案件を取得（変更前の状態を保存）
    case = db.query(CaseModel).filter(CaseModel.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="案件が見つかりません"
        )

    # 変更前のデータをコピー（変更履歴記録用）
    old_case_data = {
        'case_number': case.case_number,
        'trade_type': case.trade_type,
        'customer_id': case.customer_id,
        'supplier_name': case.supplier_name,
        'product_id': case.product_id,
        'quantity': case.quantity,
        'unit': case.unit,
        'sales_unit_price': case.sales_unit_price,
        'purchase_unit_price': case.purchase_unit_price,
        'shipment_date': case.shipment_date,
        'status': case.status,
        'pic': case.pic,
        'notes': case.notes,
    }

    # 顧客IDが変更される場合、顧客の存在確認
    if case_in.customer_id is not None and case_in.customer_id != case.customer_id:
        customer = db.query(CustomerModel).filter(CustomerModel.id == case_in.customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された顧客が見つかりません"
            )

    # 商品IDが変更される場合、商品の存在確認
    if case_in.product_id is not None and case_in.product_id != case.product_id:
        product = db.query(ProductModel).filter(ProductModel.id == case_in.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された商品が見つかりません"
            )

    # 変更内容を収集
    changes = {}
    update_data = case_in.model_dump(exclude_unset=True)

    for field, new_value in update_data.items():
        old_value = getattr(case, field, None)
        if old_value != new_value:
            changes[field] = {'old': old_value, 'new': new_value}
        setattr(case, field, new_value)

    case.updated_by = current_user.id

    # 金額を再計算
    case.calculate_amounts()

    db.commit()
    db.refresh(case)

    # 変更履歴を記録
    if changes:
        try:
            record_change_history(
                db=db,
                case_id=case.id,
                change_type="UPDATE",
                changed_by=current_user.id,
                changes=changes,
                case_number_snapshot=case.case_number
            )
            db.commit()
        except Exception as e:
            # 変更履歴記録エラーは警告のみ（案件更新は成功）
            import logging
            db.rollback()
            logging.warning(f"変更履歴の記録に失敗しました: {str(e)}")

    # リレーションを読み込んで返す
    case = db.query(CaseModel).options(
        joinedload(CaseModel.customer),
        joinedload(CaseModel.product)
    ).filter(CaseModel.id == case.id).first()

    # WebSocket通知を送信（全ユーザーに送信）
    try:
        await notify_case_updated(case.id, "updated", user_id=None)
    except Exception as e:
        import logging
        logging.warning(f"WebSocket通知の送信に失敗しました: {str(e)}")

    return case


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> None:
    """
    案件を削除

    Args:
        case_id: 案件ID
        db: データベースセッション
        current_user: 現在のユーザー

    Raises:
        HTTPException: 案件が見つからない場合
    """
    # 案件を取得
    case = db.query(CaseModel).filter(CaseModel.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="案件が見つかりません"
        )

    # 既に削除履歴が存在するかチェック（重複記録を防ぐ）
    from ...models.change_history import ChangeHistory as ChangeHistoryModel
    existing_delete_history = db.query(ChangeHistoryModel).filter(
        ChangeHistoryModel.case_id == case.id,
        ChangeHistoryModel.change_type == "DELETE"
    ).first()

    # 削除前に変更履歴を記録（まだ記録されていない場合のみ）
    import logging
    if not existing_delete_history:
        try:
            # 削除履歴を記録
            record_change_history(
                db=db,
                case_id=case.id,
                change_type="DELETE",
                changed_by=current_user.id,
                old_case=case,
                case_number_snapshot=case.case_number
            )
            # 削除履歴を確実にコミット（案件削除とは別トランザクション）
            db.commit()
            logging.info(f"削除履歴を記録しました: case_id={case.id}, case_number={case.case_number}")
        except Exception as e:
            # 変更履歴記録エラーはロールバックして警告を記録
            db.rollback()
            import traceback
            error_traceback = traceback.format_exc()
            logging.error(f"削除履歴の記録に失敗しました: case_id={case.id}, error={str(e)}\n{error_traceback}")
            # 削除履歴の記録に失敗しても案件削除は続行（警告のみ）

    # 案件を削除
    # SQLiteでは外部キー制約がデフォルトで無効のため、変更履歴は残る
    import logging
    import traceback
    from ...core.config import settings

    try:
        # 削除前にリレーションシップを確認（デバッグ用）
        logging.info(f"案件削除開始: case_id={case.id}, case_number={case.case_number}")

        # 関連する変更履歴の数を確認
        change_history_count = db.query(ChangeHistoryModel).filter(
            ChangeHistoryModel.case_id == case.id
        ).count()
        logging.info(f"関連する変更履歴数: {change_history_count}")

        # 関連するドキュメントの数を確認
        from ...models.document import Document as DocumentModel
        document_count = db.query(DocumentModel).filter(
            DocumentModel.case_id == case.id
        ).count()
        logging.info(f"関連するドキュメント数: {document_count}")

        # 案件を削除（リレーションシップは自動的に処理される）
        # documentsはcascade="all, delete-orphan"で自動削除される
        # change_historiesはcascadeがないため残る
        db.delete(case)
        db.commit()
        logging.info(f"案件削除成功: case_id={case.id}, 削除履歴は既に記録済み")
    except Exception as e:
        db.rollback()
        error_detail = str(e)
        error_traceback = traceback.format_exc()
        error_type = type(e).__name__
        logging.error(f"案件削除エラー [type={error_type}]: {error_detail}\n{error_traceback}")

        # より詳細なエラーメッセージを返す
        error_message = f"案件の削除に失敗しました"

        # エラーの種類に応じた詳細メッセージ
        if "FOREIGN KEY" in error_detail or "foreign key" in error_detail.lower():
            error_message += ": 外部キー制約エラー - 関連するデータが存在するため削除できません"
        elif "constraint" in error_detail.lower():
            error_message += ": データベースの制約に違反しています"
        elif "IntegrityError" in error_type:
            error_message += ": データベースの整合性制約に違反しています"
        elif "OperationalError" in error_type:
            error_message += f": データベース操作エラー - {error_detail}"
        else:
            error_message += f": {error_detail}"

        # デバッグ用に詳細情報も含める（開発環境のみ）
        if settings.DEBUG:
            error_message += f" (エラータイプ: {error_type})"

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )

    # WebSocket通知を送信（全ユーザーに送信）
    try:
        await notify_case_updated(case_id, "deleted", user_id=None)
    except Exception as e:
        import logging
        logging.warning(f"WebSocket通知の送信に失敗しました: {str(e)}")


# 統計情報エンドポイント（オプション）
@router.get("/stats/summary")
async def get_cases_summary(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    案件の統計情報を取得

    Args:
        db: データベースセッション
        current_user: 現在のユーザー

    Returns:
        dict: 統計情報
    """
    from sqlalchemy import func

    # 総案件数
    total_cases = db.query(func.count(CaseModel.id)).scalar()

    # ステータス別集計
    status_counts = db.query(
        CaseModel.status,
        func.count(CaseModel.id).label('count')
    ).group_by(CaseModel.status).all()

    # 区分別集計
    trade_type_counts = db.query(
        CaseModel.trade_type,
        func.count(CaseModel.id).label('count')
    ).group_by(CaseModel.trade_type).all()

    return {
        "total_cases": total_cases,
        "status_counts": {s.status: s.count for s in status_counts},
        "trade_type_counts": {t.trade_type: t.count for t in trade_type_counts}
    }
