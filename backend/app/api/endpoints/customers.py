"""
顧客マスタ API エンドポイント
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from ...core.deps import get_db, get_current_user
from ...models.user import User
from ...models.customer import Customer
from ...schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerListResponse
)

router = APIRouter()


@router.get("/", response_model=CustomerListResponse)
def get_customers(
    skip: int = Query(0, ge=0, description="スキップ件数"),
    limit: int = Query(50, ge=1, le=100, description="取得件数"),
    search: Optional[str] = Query(None, description="検索キーワード（顧客コード、顧客名）"),
    is_active: Optional[int] = Query(None, description="有効フラグフィルタ"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    顧客マスタ一覧取得
    """
    query = db.query(Customer)

    # 検索フィルタ
    if search:
        query = query.filter(
            or_(
                Customer.customer_code.ilike(f"%{search}%"),
                Customer.customer_name.ilike(f"%{search}%"),
                Customer.customer_name_en.ilike(f"%{search}%")
            )
        )

    # 有効フラグフィルタ
    if is_active is not None:
        query = query.filter(Customer.is_active == is_active)

    # 総件数
    total = query.count()

    # ページング
    customers = query.order_by(Customer.customer_code).offset(skip).limit(limit).all()

    # ページ情報計算
    page = (skip // limit) + 1
    total_pages = (total + limit - 1) // limit

    return CustomerListResponse(
        total=total,
        items=customers,
        page=page,
        page_size=limit,
        total_pages=total_pages
    )


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    顧客マスタ詳細取得
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"顧客ID {customer_id} が見つかりません"
        )
    return customer


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_in: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    顧客マスタ新規作成
    """
    # 顧客コードの重複チェック
    existing = db.query(Customer).filter(
        Customer.customer_code == customer_in.customer_code
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"顧客コード '{customer_in.customer_code}' は既に使用されています"
        )

    # 新規作成
    customer = Customer(**customer_in.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_in: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    顧客マスタ更新
    """
    # 既存データ取得
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"顧客ID {customer_id} が見つかりません"
        )

    # 顧客コードの重複チェック（更新時）
    if customer_in.customer_code and customer_in.customer_code != customer.customer_code:
        existing = db.query(Customer).filter(
            Customer.customer_code == customer_in.customer_code,
            Customer.id != customer_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"顧客コード '{customer_in.customer_code}' は既に使用されています"
            )

    # 更新
    update_data = customer_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    顧客マスタ削除（論理削除）
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"顧客ID {customer_id} が見つかりません"
        )

    # 論理削除
    customer.is_active = 0
    db.commit()

    return None


@router.get("/autocomplete/", response_model=list[CustomerResponse])
def autocomplete_customers(
    q: str = Query(..., min_length=1, description="検索キーワード"),
    limit: int = Query(10, ge=1, le=50, description="取得件数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    顧客マスタオートコンプリート
    （案件フォームでの入力補完用）
    """
    customers = db.query(Customer).filter(
        Customer.is_active == 1,
        or_(
            Customer.customer_code.ilike(f"%{q}%"),
            Customer.customer_name.ilike(f"%{q}%")
        )
    ).order_by(Customer.customer_code).limit(limit).all()

    return customers






