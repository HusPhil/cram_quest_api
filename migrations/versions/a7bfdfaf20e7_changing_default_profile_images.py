"""changing default profile images

Revision ID: a7bfdfaf20e7
Revises: 04f8fd0705f1
Create Date: 2025-04-10 11:36:45.592751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7bfdfaf20e7'
down_revision: Union[str, None] = '04f8fd0705f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Overwrite avatar_url for all profile entries
    op.execute("UPDATE profile SET avatar_url = 'default/default_1.png';")


def downgrade() -> None:
    """Downgrade schema."""
    # Revert avatar_url to NULL (you can change this if needed)
    op.execute("UPDATE profile SET avatar_url = NULL;")
