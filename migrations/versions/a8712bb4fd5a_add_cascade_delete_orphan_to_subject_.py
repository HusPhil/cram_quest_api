"""add_cascade_delete_orphan_to_subject_quests

Revision ID: a8712bb4fd5a
Revises: a7bfdfaf20e7
Create Date: 2025-04-23 23:37:13.053011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8712bb4fd5a'
down_revision: Union[str, None] = 'a7bfdfaf20e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
