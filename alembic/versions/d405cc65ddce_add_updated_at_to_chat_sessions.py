"""add_updated_at_to_chat_sessions

Revision ID: d405cc65ddce
Revises: c3d4e5f6a7b8
Create Date: 2026-03-13 17:19:55.702161

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'd405cc65ddce'
down_revision: Union[str, None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('chat_sessions', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # Initialize updated_at with created_at for existing rows
    op.execute("UPDATE chat_sessions SET updated_at = created_at WHERE updated_at IS NULL")


def downgrade() -> None:
    op.drop_column('chat_sessions', 'updated_at')
