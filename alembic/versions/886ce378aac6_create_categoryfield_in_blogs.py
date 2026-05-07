"""create categoryfield in blogs

Revision ID: 886ce378aac6
Revises: 7f28d2abd366
Create Date: 2026-05-07 05:24:01.614706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '886ce378aac6'
down_revision: Union[str, None] = '7f28d2abd366'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('blogs',sa.Column('category',sa.String(),nullable=False))


def downgrade() -> None:
    pass
