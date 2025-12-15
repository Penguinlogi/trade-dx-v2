"""Initial migration - create all tables

Revision ID: 001
Revises: 
Create Date: 2025-11-21

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ユーザーテーブル
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 顧客マスタテーブル
    op.create_table(
        'customers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_code', sa.String(length=10), nullable=False, comment='顧客コード'),
        sa.Column('customer_name', sa.String(length=100), nullable=False, comment='顧客名（日本語）'),
        sa.Column('customer_name_en', sa.String(length=200), nullable=True, comment='顧客名（英語）'),
        sa.Column('address', sa.Text(), nullable=True, comment='住所（日本語）'),
        sa.Column('address_en', sa.Text(), nullable=True, comment='住所（英語）'),
        sa.Column('phone', sa.String(length=20), nullable=True, comment='電話番号'),
        sa.Column('contact_person', sa.String(length=50), nullable=True, comment='担当者名'),
        sa.Column('email', sa.String(length=100), nullable=True, comment='メールアドレス'),
        sa.Column('payment_terms', sa.String(length=50), nullable=True, comment='支払条件'),
        sa.Column('notes', sa.Text(), nullable=True, comment='備考'),
        sa.Column('is_active', sa.Integer(), nullable=False, server_default='1', comment='有効フラグ（1=有効, 0=無効）'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customers_id'), 'customers', ['id'], unique=False)
    op.create_index(op.f('ix_customers_customer_code'), 'customers', ['customer_code'], unique=True)

    # 商品マスタテーブル
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_code', sa.String(length=10), nullable=False, comment='商品コード'),
        sa.Column('product_name', sa.String(length=100), nullable=False, comment='商品名（日本語）'),
        sa.Column('product_name_en', sa.String(length=200), nullable=True, comment='商品名（英語）'),
        sa.Column('hs_code', sa.String(length=20), nullable=True, comment='HSコード'),
        sa.Column('unit', sa.String(length=10), nullable=True, comment='単位（kg, pcs, m3, etc.）'),
        sa.Column('standard_price', sa.Numeric(precision=15, scale=2), nullable=True, comment='標準単価'),
        sa.Column('category', sa.String(length=50), nullable=True, comment='カテゴリ'),
        sa.Column('specification', sa.Text(), nullable=True, comment='仕様・スペック'),
        sa.Column('notes', sa.Text(), nullable=True, comment='備考'),
        sa.Column('is_active', sa.Integer(), nullable=False, server_default='1', comment='有効フラグ（1=有効, 0=無効）'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_index(op.f('ix_products_product_code'), 'products', ['product_code'], unique=True)

    # 案件番号管理テーブル
    op.create_table(
        'case_numbers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False, comment='年（YYYY）'),
        sa.Column('trade_type', sa.String(length=10), nullable=False, comment='区分（輸出/輸入）'),
        sa.Column('trade_type_code', sa.String(length=2), nullable=False, comment='区分コード（EX/IM）'),
        sa.Column('last_sequence', sa.Integer(), nullable=False, server_default='0', comment='最後に使用した連番'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_case_numbers_id'), 'case_numbers', ['id'], unique=False)
    op.create_index(op.f('ix_case_numbers_year'), 'case_numbers', ['year'], unique=False)
    op.create_index(op.f('ix_case_numbers_trade_type'), 'case_numbers', ['trade_type'], unique=False)

    # バックアップ履歴テーブル
    op.create_table(
        'backups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('backup_name', sa.String(length=100), nullable=False, comment='バックアップ名'),
        sa.Column('backup_path', sa.String(length=500), nullable=False, comment='バックアップファイルパス'),
        sa.Column('backup_type', sa.String(length=20), nullable=False, comment='バックアップタイプ（manual/auto/scheduled）'),
        sa.Column('file_size', sa.BigInteger(), nullable=True, comment='ファイルサイズ（バイト）'),
        sa.Column('record_count', sa.Integer(), nullable=True, comment='レコード数'),
        sa.Column('status', sa.String(length=20), nullable=False, comment='ステータス（success/failed/in_progress）'),
        sa.Column('error_message', sa.Text(), nullable=True, comment='エラーメッセージ'),
        sa.Column('created_by', sa.Integer(), nullable=True, comment='作成者ID'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_backups_id'), 'backups', ['id'], unique=False)
    op.create_index(op.f('ix_backups_created_at'), 'backups', ['created_at'], unique=False)

    # 案件テーブル
    op.create_table(
        'cases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_number', sa.String(length=20), nullable=False, comment='案件番号 (例: 2025-EX-001)'),
        sa.Column('trade_type', sa.String(length=10), nullable=False, comment='区分（輸出/輸入）'),
        sa.Column('customer_id', sa.Integer(), nullable=False, comment='顧客ID'),
        sa.Column('supplier_name', sa.String(length=100), nullable=True, comment='仕入先名'),
        sa.Column('product_id', sa.Integer(), nullable=False, comment='商品ID'),
        sa.Column('quantity', sa.Numeric(precision=15, scale=3), nullable=False, comment='数量'),
        sa.Column('unit', sa.String(length=10), nullable=False, comment='単位'),
        sa.Column('sales_unit_price', sa.Numeric(precision=15, scale=2), nullable=False, comment='販売単価'),
        sa.Column('purchase_unit_price', sa.Numeric(precision=15, scale=2), nullable=False, comment='仕入単価'),
        sa.Column('sales_amount', sa.Numeric(precision=15, scale=2), nullable=True, comment='売上額（計算値）'),
        sa.Column('gross_profit', sa.Numeric(precision=15, scale=2), nullable=True, comment='粗利額（計算値）'),
        sa.Column('gross_profit_rate', sa.Numeric(precision=5, scale=2), nullable=True, comment='粗利率%（計算値）'),
        sa.Column('shipment_date', sa.Date(), nullable=True, comment='船積予定日'),
        sa.Column('status', sa.String(length=20), nullable=False, comment='ステータス（見積中/受注済/船積済/完了/キャンセル）'),
        sa.Column('pic', sa.String(length=50), nullable=False, comment='担当者名'),
        sa.Column('notes', sa.Text(), nullable=True, comment='備考'),
        sa.Column('created_by', sa.Integer(), nullable=True, comment='作成者ID'),
        sa.Column('updated_by', sa.Integer(), nullable=True, comment='更新者ID'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cases_id'), 'cases', ['id'], unique=False)
    op.create_index(op.f('ix_cases_case_number'), 'cases', ['case_number'], unique=True)

    # 変更履歴テーブル
    op.create_table(
        'change_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), nullable=False, comment='案件ID'),
        sa.Column('changed_by', sa.Integer(), nullable=True, comment='変更者ID'),
        sa.Column('change_type', sa.String(length=20), nullable=False, comment='変更タイプ（CREATE/UPDATE/DELETE）'),
        sa.Column('field_name', sa.String(length=50), nullable=True, comment='変更フィールド名'),
        sa.Column('old_value', sa.Text(), nullable=True, comment='変更前の値'),
        sa.Column('new_value', sa.Text(), nullable=True, comment='変更後の値'),
        sa.Column('changes_json', sa.JSON(), nullable=True, comment='変更詳細（JSON）'),
        sa.Column('notes', sa.Text(), nullable=True, comment='備考'),
        sa.Column('changed_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.ForeignKeyConstraint(['changed_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_change_history_id'), 'change_history', ['id'], unique=False)
    op.create_index(op.f('ix_change_history_case_id'), 'change_history', ['case_id'], unique=False)
    op.create_index(op.f('ix_change_history_changed_at'), 'change_history', ['changed_at'], unique=False)


def downgrade() -> None:
    op.drop_table('change_history')
    op.drop_table('cases')
    op.drop_table('backups')
    op.drop_table('case_numbers')
    op.drop_table('products')
    op.drop_table('customers')
    op.drop_table('users')












