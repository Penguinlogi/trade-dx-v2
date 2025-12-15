"""
データベース確認スクリプト

データベース内のデータを確認します。
"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import inspect, text
from app.core.database import SessionLocal, engine
from app.models import User, Customer, Product, CaseNumber, Case


def check_users(db):
    """ユーザーテーブルを確認"""
    print("\n" + "=" * 80)
    print("ユーザーテーブル (users)")
    print("=" * 80)
    
    users = db.query(User).all()
    
    if not users:
        print("データがありません")
        return
    
    print(f"{'ID':<5} {'ユーザー名':<15} {'メールアドレス':<30} {'フルネーム':<15} {'アクティブ':<10} {'管理者':<10}")
    print("-" * 80)
    
    for user in users:
        print(f"{user.id:<5} {user.username:<15} {user.email:<30} {user.full_name or '':<15} "
              f"{'○' if user.is_active else '×':<10} {'○' if user.is_superuser else '×':<10}")
    
    print(f"\n合計: {len(users)} 件")


def check_customers(db):
    """顧客マスタを確認"""
    print("\n" + "=" * 80)
    print("顧客マスタ (customers)")
    print("=" * 80)
    
    customers = db.query(Customer).all()
    
    if not customers:
        print("データがありません")
        return
    
    print(f"{'ID':<5} {'顧客コード':<12} {'顧客名':<30} {'担当者':<15}")
    print("-" * 80)
    
    for customer in customers:
        print(f"{customer.id:<5} {customer.customer_code:<12} {customer.customer_name:<30} "
              f"{customer.contact_person or '':<15}")
    
    print(f"\n合計: {len(customers)} 件")


def check_products(db):
    """商品マスタを確認"""
    print("\n" + "=" * 80)
    print("商品マスタ (products)")
    print("=" * 80)
    
    products = db.query(Product).all()
    
    if not products:
        print("データがありません")
        return
    
    print(f"{'ID':<5} {'商品コード':<12} {'商品名':<30} {'単位':<8} {'標準価格':<12}")
    print("-" * 80)
    
    for product in products:
        print(f"{product.id:<5} {product.product_code:<12} {product.product_name:<30} "
              f"{product.unit or '':<8} {product.standard_price or 0:<12.2f}")
    
    print(f"\n合計: {len(products)} 件")


def check_case_numbers(db):
    """案件番号管理を確認"""
    print("\n" + "=" * 80)
    print("案件番号管理 (case_numbers)")
    print("=" * 80)
    
    case_numbers = db.query(CaseNumber).all()
    
    if not case_numbers:
        print("データがありません")
        return
    
    print(f"{'ID':<5} {'年度':<8} {'貿易種別':<12} {'コード':<8} {'最終連番':<12}")
    print("-" * 80)
    
    for cn in case_numbers:
        print(f"{cn.id:<5} {cn.year:<8} {cn.trade_type:<12} {cn.trade_type_code:<8} {cn.last_sequence:<12}")
    
    print(f"\n合計: {len(case_numbers)} 件")


def check_cases(db):
    """案件を確認"""
    print("\n" + "=" * 80)
    print("案件 (cases)")
    print("=" * 80)
    
    cases = db.query(Case).all()
    
    if not cases:
        print("データがありません")
        return
    
    print(f"{'ID':<5} {'案件番号':<15} {'区分':<8} {'顧客ID':<8} {'商品ID':<8} "
          f"{'数量':<10} {'ステータス':<12} {'担当者':<12}")
    print("-" * 80)
    
    for case in cases:
        print(f"{case.id:<5} {case.case_number:<15} {case.trade_type:<8} "
              f"{case.customer_id:<8} {case.product_id:<8} "
              f"{str(case.quantity):<10} {case.status:<12} {case.pic:<12}")
    
    print(f"\n合計: {len(cases)} 件")


def check_all_tables():
    """すべてのテーブルを確認"""
    print("=" * 80)
    print("貿易DX データベース確認")
    print("=" * 80)
    
    # テーブル一覧を表示
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"\nテーブル一覧: {', '.join(tables)}")
    
    # データベースセッション
    db = SessionLocal()
    
    try:
        # 各テーブルを確認
        check_users(db)
        check_customers(db)
        check_products(db)
        check_case_numbers(db)
        check_cases(db)
        
        print("\n" + "=" * 80)
        print("✓ データベース確認完了")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ エラーが発生しました: {e}")
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    check_all_tables()


