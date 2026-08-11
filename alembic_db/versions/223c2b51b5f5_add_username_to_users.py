"""add username to users

Revision ID: 223c2b51b5f5
Revises: c234fd408fa1
Create Date: 2026-08-11 21:34:20.470856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '223c2b51b5f5'
down_revision: Union[str, Sequence[str], None] = 'c234fd408fa1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('username', sa.String(), nullable=True)
    )

    op.execute(
        "UPDATE users SET username = 'user_' || id"
    )

    op.alter_column(
        'users',
        'username',
        nullable=False
    )

    op.create_unique_constraint(
        'uq_users_username',
        'users',
        ['username']
    )


def downgrade() -> None:
    op.drop_constraint(
        'uq_users_username',
        'users',
        type_='unique'
    )

    op.drop_column('users', 'username')
