"""Creating vote tables

Revision ID: 3381756eeced
Revises: 20e692f4130a
Create Date: 2025-01-07 21:59:13.062018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3381756eeced'
down_revision: Union[str, None] = '20e692f4130a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    print("Running upgrade migration...")
    op.create_table(
        'votes',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    print("Votes table created successfully!")

def downgrade() -> None:
    print("Running downgrade migration...")
    op.drop_table('votes')
    print("Votes table dropped successfully!")
