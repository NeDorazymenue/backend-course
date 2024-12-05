"""add users

Revision ID: f3a0809019df
Revises: 89c393cba467
Create Date: 2024-11-20 17:08:58.358767

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f3a0809019df"
down_revision: Union[str, None] = "89c393cba467"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("password", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
