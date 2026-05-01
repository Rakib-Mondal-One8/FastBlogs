"""created ForeignKey in Blogs Model

Revision ID: 20dee2440ccc
Revises: 
Create Date: 2026-04-30 18:51:21.181181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20dee2440ccc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('blogs',sa.Column('owner_id',sa.Integer(),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('blogs','user_id')