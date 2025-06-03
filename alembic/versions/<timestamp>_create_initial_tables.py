"""create initial tables"""

from alembic import op
import sqlalchemy as sa

# Обязательные переменные для Alembic
revision = '202406021200'  # Уникальный ID этой миграции (можно любой, но лучше timestamp)
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('hashed_password', sa.String, nullable=False)
    )

    op.create_table('readers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True)
    )

    op.create_table('books',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('author', sa.String, nullable=False),
        sa.Column('year', sa.Integer),
        sa.Column('isbn', sa.String, unique=True),
        sa.Column('count', sa.Integer, nullable=False, server_default='1')
    )

    op.create_table('borrowed_books',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('book_id', sa.Integer, sa.ForeignKey('books.id')),
        sa.Column('reader_id', sa.Integer, sa.ForeignKey('readers.id')),
        sa.Column('borrow_date', sa.DateTime, nullable=False),
        sa.Column('return_date', sa.DateTime, nullable=True)
    )

def downgrade():
    op.drop_table('borrowed_books')
    op.drop_table('books')
    op.drop_table('readers')
    op.drop_table('users')
