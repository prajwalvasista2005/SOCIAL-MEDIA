"""add content column to posts table

Revision ID: 1368eb076d8f
Revises: 4216f769ebd7
Create Date: 2026-08-11 12:44:00.693830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1368eb076d8f'
down_revision: Union[str, Sequence[str], None] = '4216f769ebd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
