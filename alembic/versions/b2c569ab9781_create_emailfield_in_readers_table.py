"""create emailfield in Readers table

Revision ID: b2c569ab9781
Revises: 
Create Date: 2026-05-07 02:15:24.782053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c569ab9781'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('readers',sa.Column('email',sa.String(),nullable=False))


def downgrade() -> None:
    pass
