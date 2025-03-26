"""Update player model with PlayerTitle enum and CASCADE

Revision ID: 2c466e70f1bb
Revises: 79c5a9316787
Create Date: 2025-03-26 08:52:10.164939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c466e70f1bb'
down_revision: Union[str, None] = '79c5a9316787'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Step 1: Create a new player table with the correct constraints
    op.create_table(
        "player_temp",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("title", sa.String, nullable=False, default="Novice"),
        sa.Column("level", sa.Integer, nullable=False, default=1),
        sa.Column("experience", sa.Integer, nullable=False, default=0),
    )

    # Step 2: Copy data from old `player` table to `player_temp`
    op.execute("INSERT INTO player_temp SELECT * FROM player")

    # Step 3: Drop the old `player` table
    op.drop_table("player")

    # Step 4: Rename `player_temp` to `player`
    op.rename_table("player_temp", "player")


def downgrade():
    # Step 1: Recreate the original `player` table without CASCADE
    op.create_table(
        "player_old",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False, unique=True),
        sa.Column("title", sa.String, nullable=False, default="Novice"),
        sa.Column("level", sa.Integer, nullable=False, default=1),
        sa.Column("experience", sa.Integer, nullable=False, default=0),
    )

    # Step 2: Copy data back from `player` to `player_old`
    op.execute("INSERT INTO player_old SELECT * FROM player")

    # Step 3: Drop the modified `player` table
    op.drop_table("player")

    # Step 4: Rename `player_old` back to `player`
    op.rename_table("player_old", "player")
