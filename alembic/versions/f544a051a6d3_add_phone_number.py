"""Add phone number

Revision ID: f544a051a6d3
Revises: 3381756eeced
Create Date: 2025-01-07 23:50:23.646078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f544a051a6d3'
down_revision: Union[str, None] = '3381756eeced'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
