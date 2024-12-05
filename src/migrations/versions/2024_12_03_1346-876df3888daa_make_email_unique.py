"""make email unique

Revision ID: 876df3888daa
Revises: 753ef4edee7d
Create Date: 2024-12-03 13:46:15.425858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '876df3888daa'
down_revision: Union[str, None] = '753ef4edee7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, 'users', ['email'])


def downgrade() -> None:
    op.drop_constraint(None, 'users', type_='unique')

