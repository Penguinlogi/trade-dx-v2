"""modify change_history case_id nullable

Revision ID: 002
Revises: 001
Create Date: 2025-11-28

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # change_historyテーブルのcase_idカラムをnullable=Trueに変更
    # SQLiteではALTER TABLEでカラムのNULL制約を変更できないため、
    # テーブルを再作成する方法を使用

    # 既存のデータを保持するため、一時テーブルにコピー
    op.execute("""
        CREATE TABLE change_history_new (
            id INTEGER NOT NULL PRIMARY KEY,
            case_id INTEGER,
            changed_by INTEGER,
            change_type VARCHAR(20) NOT NULL,
            field_name VARCHAR(50),
            old_value TEXT,
            new_value TEXT,
            changes_json JSON,
            notes TEXT,
            changed_at DATETIME NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE SET NULL,
            FOREIGN KEY (changed_by) REFERENCES users(id)
        )
    """)

    # 既存データをコピー
    op.execute("""
        INSERT INTO change_history_new
        SELECT * FROM change_history
    """)

    # 古いテーブルを削除
    op.drop_table('change_history')

    # 新しいテーブルをリネーム
    op.execute("""
        ALTER TABLE change_history_new RENAME TO change_history
    """)

    # インデックスを再作成
    op.create_index('ix_change_history_id', 'change_history', ['id'], unique=False)
    op.create_index('ix_change_history_case_id', 'change_history', ['case_id'], unique=False)
    op.create_index('ix_change_history_changed_at', 'change_history', ['changed_at'], unique=False)


def downgrade() -> None:
    # ダウングレード時は、case_idをnullable=Falseに戻す
    op.execute("""
        CREATE TABLE change_history_old (
            id INTEGER NOT NULL PRIMARY KEY,
            case_id INTEGER NOT NULL,
            changed_by INTEGER,
            change_type VARCHAR(20) NOT NULL,
            field_name VARCHAR(50),
            old_value TEXT,
            new_value TEXT,
            changes_json JSON,
            notes TEXT,
            changed_at DATETIME NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(id),
            FOREIGN KEY (changed_by) REFERENCES users(id)
        )
    """)

    # case_idがNULLのレコードは除外してコピー
    op.execute("""
        INSERT INTO change_history_old
        SELECT * FROM change_history
        WHERE case_id IS NOT NULL
    """)

    op.drop_table('change_history')
    op.execute("""
        ALTER TABLE change_history_old RENAME TO change_history
    """)

    op.create_index('ix_change_history_id', 'change_history', ['id'], unique=False)
    op.create_index('ix_change_history_case_id', 'change_history', ['case_id'], unique=False)
    op.create_index('ix_change_history_changed_at', 'change_history', ['changed_at'], unique=False)






