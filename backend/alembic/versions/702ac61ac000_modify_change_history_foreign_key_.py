"""modify_change_history_foreign_key_ondelete_setnull

Revision ID: 702ac61ac000
Revises: 002
Create Date: 2025-12-17 10:48:18.055011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '702ac61ac000'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # PostgreSQL用: change_historyテーブルの外部キー制約をON DELETE SET NULLに変更
    # まず、既存の外部キー制約を削除
    op.drop_constraint('change_history_case_id_fkey', 'change_history', type_='foreignkey')

    # case_idカラムをnullable=Trueに変更（PostgreSQL用）
    op.alter_column('change_history', 'case_id',
                    existing_type=sa.Integer(),
                    nullable=True,
                    existing_nullable=False)

    # 新しい外部キー制約を追加（ON DELETE SET NULL）
    op.create_foreign_key(
        'change_history_case_id_fkey',
        'change_history', 'cases',
        ['case_id'], ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    # ダウングレード時は、外部キー制約を元に戻す
    op.drop_constraint('change_history_case_id_fkey', 'change_history', type_='foreignkey')

    # case_idがNULLのレコードを削除（ダウングレード時）
    op.execute("DELETE FROM change_history WHERE case_id IS NULL")

    # case_idカラムをnullable=Falseに戻す
    op.alter_column('change_history', 'case_id',
                    existing_type=sa.Integer(),
                    nullable=False,
                    existing_nullable=True)

    # 元の外部キー制約を追加
    op.create_foreign_key(
        'change_history_case_id_fkey',
        'change_history', 'cases',
        ['case_id'], ['id']
    )
