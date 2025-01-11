"""Adding another column

Revision ID: 892f01d9e560
Revises: 1934afc69bdd
Create Date: 2025-01-03 22:34:25.163133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '892f01d9e560'
down_revision: Union[str, None] = '1934afc69bdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
