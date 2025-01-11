"""Adding foreign key

Revision ID: 0fa2717b8c9e
Revises: f732cad9fb14
Create Date: 2025-01-06 00:08:15.414237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fa2717b8c9e'
down_revision: Union[str, None] = 'f732cad9fb14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=True))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass

def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name="posts")
    op.drop_table('posts','owner_id')
    pass
