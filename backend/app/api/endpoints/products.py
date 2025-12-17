"""
商品マスタ API エンドポイント
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from ...core.deps import get_db, get_current_user
from ...models.user import User
from ...models.product import Product
from ...schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse
)

router = APIRouter()


@router.get("/", response_model=ProductListResponse)
def get_products(
    skip: int = Query(0, ge=0, description="スキップ件数"),
    limit: int = Query(50, ge=1, le=100, description="取得件数"),
    search: Optional[str] = Query(None, description="検索キーワード（商品コード、商品名）"),
    category: Optional[str] = Query(None, description="カテゴリフィルタ"),
    is_active: Optional[int] = Query(None, description="有効フラグフィルタ"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    商品マスタ一覧取得
    """
    query = db.query(Product)

    # 検索フィルタ
    if search:
        query = query.filter(
            or_(
                Product.product_code.ilike(f"%{search}%"),
                Product.product_name.ilike(f"%{search}%"),
                Product.product_name_en.ilike(f"%{search}%")
            )
        )

    # カテゴリフィルタ
    if category:
        query = query.filter(Product.category == category)

    # 有効フラグフィルタ
    if is_active is not None:
        query = query.filter(Product.is_active == is_active)

    # 総件数
    total = query.count()

    # ページング
    products = query.order_by(Product.product_code).offset(skip).limit(limit).all()

    # ページ情報計算
    page = (skip // limit) + 1
    total_pages = (total + limit - 1) // limit

    return ProductListResponse(
        total=total,
        items=products,
        page=page,
        page_size=limit,
        total_pages=total_pages
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    商品マスタ詳細取得
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"商品ID {product_id} が見つかりません"
        )
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    商品マスタ新規作成
    """
    # 商品コードの重複チェック
    existing = db.query(Product).filter(
        Product.product_code == product_in.product_code
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"商品コード '{product_in.product_code}' は既に使用されています"
        )

    # 新規作成
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    商品マスタ更新
    """
    # 既存データ取得
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"商品ID {product_id} が見つかりません"
        )

    # 商品コードの重複チェック（更新時）
    if product_in.product_code and product_in.product_code != product.product_code:
        existing = db.query(Product).filter(
            Product.product_code == product_in.product_code,
            Product.id != product_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"商品コード '{product_in.product_code}' は既に使用されています"
            )

    # 更新
    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    商品マスタ削除（論理削除）
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"商品ID {product_id} が見つかりません"
        )

    # 論理削除
    product.is_active = 0
    db.commit()

    return None


@router.get("/autocomplete/", response_model=list[ProductResponse])
def autocomplete_products(
    q: str = Query(..., min_length=1, description="検索キーワード"),
    limit: int = Query(10, ge=1, le=50, description="取得件数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    商品マスタオートコンプリート
    （案件フォームでの入力補完用）
    """
    products = db.query(Product).filter(
        Product.is_active == 1,
        or_(
            Product.product_code.ilike(f"%{q}%"),
            Product.product_name.ilike(f"%{q}%")
        )
    ).order_by(Product.product_code).limit(limit).all()

    return products


@router.get("/categories/", response_model=list[str])
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    カテゴリ一覧取得（ユニークなカテゴリ名を取得）
    """
    categories = db.query(Product.category).filter(
        Product.category.isnot(None),
        Product.is_active == 1
    ).distinct().order_by(Product.category).all()

    return [cat[0] for cat in categories if cat[0]]








