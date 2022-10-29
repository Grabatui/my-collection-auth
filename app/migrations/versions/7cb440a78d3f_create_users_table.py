"""create_users_table

Revision ID: 7cb440a78d3f
Revises: 
Create Date: 2022-10-21 06:49:58.691523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cb440a78d3f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer),
        sa.Column('username', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('inserted_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('source', sa.String, nullable=False),

        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('users')
