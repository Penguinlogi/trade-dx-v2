"""
シードデータ投入スクリプト

基本的なマスタデータと初期ユーザーを作成します。
"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime, date
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core.database import SessionLocal, engine, Base
from app.models import User, Customer, Product, CaseNumber

# パスワードハッシュ化
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_tables():
    """テーブルを作成"""
    print("テーブルを作成中...")
    Base.metadata.create_all(bind=engine)
    print("✓ テーブル作成完了")


def seed_users(db: Session):
    """初期ユーザーを作成"""
    print("\n初期ユーザーを作成中...")
    
    users = [
        User(
            username="admin",
            email="admin@example.com",
            hashed_password=pwd_context.hash("admin123"),
            full_name="管理者",
            is_active=True,
            is_superuser=True,
        ),
        User(
            username="yamada",
            email="yamada@example.com",
            hashed_password=pwd_context.hash("yamada123"),
            full_name="山田太郎",
            is_active=True,
            is_superuser=False,
        ),
        User(
            username="suzuki",
            email="suzuki@example.com",
            hashed_password=pwd_context.hash("suzuki123"),
            full_name="鈴木花子",
            is_active=True,
            is_superuser=False,
        ),
    ]
    
    for user in users:
        existing = db.query(User).filter(User.username == user.username).first()
        if not existing:
            db.add(user)
            print(f"  - {user.username} ({user.full_name})")
    
    db.commit()
    print("✓ ユーザー作成完了")


def seed_customers(db: Session):
    """顧客マスタを作成"""
    print("\n顧客マスタを作成中...")
    
    customers = [
        Customer(
            customer_code="C001",
            customer_name="ABC商事株式会社",
            customer_name_en="ABC Trading Co., Ltd.",
            address="東京都千代田区丸の内1-1-1",
            address_en="1-1-1 Marunouchi, Chiyoda-ku, Tokyo, Japan",
            phone="03-1234-5678",
            contact_person="田中一郎",
            email="tanaka@abc-trading.co.jp",
            payment_terms="月末締め翌月末払い",
            is_active=1,
        ),
        Customer(
            customer_code="C002",
            customer_name="XYZ物産株式会社",
            customer_name_en="XYZ Corporation",
            address="大阪府大阪市北区梅田2-2-2",
            address_en="2-2-2 Umeda, Kita-ku, Osaka, Japan",
            phone="06-9876-5432",
            contact_person="佐藤花子",
            email="sato@xyz-corp.co.jp",
            payment_terms="月末締め翌々月10日払い",
            is_active=1,
        ),
        Customer(
            customer_code="C003",
            customer_name="グローバル貿易株式会社",
            customer_name_en="Global Trade Inc.",
            address="神奈川県横浜市西区みなとみらい3-3-3",
            address_en="3-3-3 Minatomirai, Nishi-ku, Yokohama, Kanagawa, Japan",
            phone="045-1111-2222",
            contact_person="高橋次郎",
            email="takahashi@global-trade.co.jp",
            payment_terms="月末締め翌月20日払い",
            is_active=1,
        ),
    ]
    
    for customer in customers:
        existing = db.query(Customer).filter(Customer.customer_code == customer.customer_code).first()
        if not existing:
            db.add(customer)
            print(f"  - {customer.customer_code}: {customer.customer_name}")
    
    db.commit()
    print("✓ 顧客マスタ作成完了")


def seed_products(db: Session):
    """商品マスタを作成"""
    print("\n商品マスタを作成中...")
    
    products = [
        Product(
            product_code="P001",
            product_name="電子部品A",
            product_name_en="Electronic Component A",
            hs_code="8542.31.000",
            unit="pcs",
            standard_price=150.00,
            category="電子部品",
            specification="サイズ: 10mm×10mm, 動作温度: -40～85℃",
            is_active=1,
        ),
        Product(
            product_code="P002",
            product_name="プラスチック原料B",
            product_name_en="Plastic Material B",
            hs_code="3901.10.000",
            unit="kg",
            standard_price=250.00,
            category="化学製品",
            specification="密度: 0.92 g/cm³, 融点: 130℃",
            is_active=1,
        ),
        Product(
            product_code="P003",
            product_name="金属パーツC",
            product_name_en="Metal Parts C",
            hs_code="7326.90.000",
            unit="pcs",
            standard_price=500.00,
            category="金属製品",
            specification="材質: ステンレス鋼, 重量: 0.5kg",
            is_active=1,
        ),
        Product(
            product_code="P004",
            product_name="繊維製品D",
            product_name_en="Textile Product D",
            hs_code="5407.10.000",
            unit="m",
            standard_price=80.00,
            category="繊維",
            specification="幅: 150cm, 素材: ポリエステル100%",
            is_active=1,
        ),
    ]
    
    for product in products:
        existing = db.query(Product).filter(Product.product_code == product.product_code).first()
        if not existing:
            db.add(product)
            print(f"  - {product.product_code}: {product.product_name}")
    
    db.commit()
    print("✓ 商品マスタ作成完了")


def seed_case_numbers(db: Session):
    """案件番号管理の初期化"""
    print("\n案件番号管理を初期化中...")
    
    current_year = datetime.now().year
    
    case_numbers = [
        CaseNumber(
            year=current_year,
            trade_type="輸出",
            trade_type_code="EX",
            last_sequence=0,
        ),
        CaseNumber(
            year=current_year,
            trade_type="輸入",
            trade_type_code="IM",
            last_sequence=0,
        ),
    ]
    
    for case_number in case_numbers:
        existing = db.query(CaseNumber).filter(
            CaseNumber.year == case_number.year,
            CaseNumber.trade_type == case_number.trade_type
        ).first()
        if not existing:
            db.add(case_number)
            print(f"  - {case_number.year}-{case_number.trade_type_code}: 連番初期化")
    
    db.commit()
    print("✓ 案件番号管理初期化完了")


def main():
    """メイン処理"""
    print("=" * 60)
    print("シードデータ投入スクリプト")
    print("=" * 60)
    
    # テーブル作成
    create_tables()
    
    # データベースセッション
    db = SessionLocal()
    
    try:
        # シードデータ投入
        seed_users(db)
        seed_customers(db)
        seed_products(db)
        seed_case_numbers(db)
        
        print("\n" + "=" * 60)
        print("✓ すべてのシードデータ投入が完了しました")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ エラーが発生しました: {e}")
        db.rollback()
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    main()














