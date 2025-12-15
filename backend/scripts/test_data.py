"""
テストデータ投入スクリプト

開発・テスト用の案件データを作成します。
"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import Case, Customer, Product, User, ChangeHistory


def create_test_cases(db: Session):
    """テスト用の案件データを作成"""
    print("テスト用案件データを作成中...")
    
    # 既存データの取得
    customers = db.query(Customer).all()
    products = db.query(Product).all()
    users = db.query(User).all()
    
    if not customers or not products or not users:
        print("✗ エラー: 顧客、商品、またはユーザーのマスタデータが存在しません")
        print("   先に seed_data.py を実行してください")
        return
    
    # テスト案件データ
    current_year = datetime.now().year
    today = date.today()
    
    test_cases = [
        Case(
            case_number=f"{current_year}-EX-001",
            trade_type="輸出",
            customer_id=customers[0].id,
            supplier_name="国内メーカーA",
            product_id=products[0].id,
            quantity=1000,
            unit="pcs",
            sales_unit_price=200.00,
            purchase_unit_price=150.00,
            shipment_date=today + timedelta(days=30),
            status="見積中",
            pic="山田太郎",
            notes="初回取引につき注意",
            created_by=users[1].id if len(users) > 1 else users[0].id,
        ),
        Case(
            case_number=f"{current_year}-EX-002",
            trade_type="輸出",
            customer_id=customers[1].id if len(customers) > 1 else customers[0].id,
            supplier_name="国内メーカーB",
            product_id=products[1].id if len(products) > 1 else products[0].id,
            quantity=500,
            unit="kg",
            sales_unit_price=300.00,
            purchase_unit_price=250.00,
            shipment_date=today + timedelta(days=20),
            status="受注済",
            pic="鈴木花子",
            notes="",
            created_by=users[2].id if len(users) > 2 else users[0].id,
        ),
        Case(
            case_number=f"{current_year}-IM-001",
            trade_type="輸入",
            customer_id=customers[2].id if len(customers) > 2 else customers[0].id,
            supplier_name="海外サプライヤーX",
            product_id=products[2].id if len(products) > 2 else products[0].id,
            quantity=200,
            unit="pcs",
            sales_unit_price=600.00,
            purchase_unit_price=500.00,
            shipment_date=today + timedelta(days=45),
            status="船積済",
            pic="山田太郎",
            notes="通関手続き中",
            created_by=users[1].id if len(users) > 1 else users[0].id,
        ),
        Case(
            case_number=f"{current_year}-EX-003",
            trade_type="輸出",
            customer_id=customers[0].id,
            supplier_name="国内メーカーC",
            product_id=products[3].id if len(products) > 3 else products[0].id,
            quantity=1500,
            unit="m",
            sales_unit_price=120.00,
            purchase_unit_price=80.00,
            shipment_date=today - timedelta(days=10),
            status="完了",
            pic="鈴木花子",
            notes="リピート注文期待",
            created_by=users[2].id if len(users) > 2 else users[0].id,
        ),
        Case(
            case_number=f"{current_year}-IM-002",
            trade_type="輸入",
            customer_id=customers[1].id if len(customers) > 1 else customers[0].id,
            supplier_name="海外サプライヤーY",
            product_id=products[0].id,
            quantity=800,
            unit="pcs",
            sales_unit_price=180.00,
            purchase_unit_price=150.00,
            shipment_date=today + timedelta(days=60),
            status="見積中",
            pic="山田太郎",
            notes="価格交渉中",
            created_by=users[1].id if len(users) > 1 else users[0].id,
        ),
    ]
    
    created_count = 0
    for case in test_cases:
        existing = db.query(Case).filter(Case.case_number == case.case_number).first()
        if not existing:
            # 金額を計算
            case.calculate_amounts()
            db.add(case)
            created_count += 1
            print(f"  - {case.case_number}: {case.status}")
    
    db.commit()
    print(f"✓ テスト案件データ作成完了 ({created_count}件)")


def main():
    """メイン処理"""
    print("=" * 60)
    print("テストデータ投入スクリプト")
    print("=" * 60)
    
    # データベースセッション
    db = SessionLocal()
    
    try:
        create_test_cases(db)
        
        # データ件数を表示
        print("\n現在のデータ件数:")
        print(f"  - ユーザー: {db.query(User).count()}件")
        print(f"  - 顧客: {db.query(Customer).count()}件")
        print(f"  - 商品: {db.query(Product).count()}件")
        print(f"  - 案件: {db.query(Case).count()}件")
        
        print("\n" + "=" * 60)
        print("✓ テストデータ投入が完了しました")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ エラーが発生しました: {e}")
        db.rollback()
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    main()












