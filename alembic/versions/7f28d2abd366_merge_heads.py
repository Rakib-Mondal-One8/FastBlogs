"""merge heads

Revision ID: 7f28d2abd366
Revises: 20dee2440ccc, b2c569ab9781
Create Date: 2026-05-07 05:23:57.789568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f28d2abd366'
down_revision: Union[str, None] = ('20dee2440ccc', 'b2c569ab9781')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
