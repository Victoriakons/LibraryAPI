"""add description to books"""

from alembic import op
import sqlalchemy as sa

# Обязательно укажи эти идентификаторы
revision = '202406021230'      # ← Уникальный ID миграции (любой, но уникальный)
down_revision = '202406021200'  # ← ID предыдущей миграции, если есть, иначе None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name='books' AND column_name='description'
        ) THEN
            ALTER TABLE books ADD COLUMN description TEXT;
            UPDATE books SET description = 'No description provided' WHERE description IS NULL;
        END IF;
    END
    $$;
    """)



def downgrade():
    op.drop_column('books', 'description')