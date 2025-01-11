"""create post table

Revision ID: 1934afc69bdd
Revises: 
Create Date: 2025-01-03 19:44:39.791343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1934afc69bdd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),primary_key=True,nullable=True),sa.Column('title',sa.String(),nullable=True))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass