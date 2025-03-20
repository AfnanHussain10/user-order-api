"""Create user_order_db

Revision ID: da85a08e4acb
Revises: 6f500bc7038c
Create Date: 2025-03-20 14:49:30.752467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da85a08e4acb'
down_revision: Union[str, None] = '6f500bc7038c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the user_order_db database and tables."""
    op.execute("CREATE DATABASE user_order_db;")

def downgrade() -> None:
    """Drop the user_order_db database if needed."""
    op.execute("DROP DATABASE IF EXISTS user_order_db;")
