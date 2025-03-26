"""Add cascade delete to player.user_id

Revision ID: 79c5a9316787
Revises: 60add319ece3
Create Date: 2025-03-26 08:04:57.724088
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "79c5a9316787"
down_revision = "60add319ece3"
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Create new `player_temp` table with CASCADE delete
    op.create_table(
        "player_temp",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("title", sa.String, nullable=False, default="Noobie"),
        sa.Column("level", sa.Integer, nullable=False, default=1),
        sa.Column("experience", sa.Integer, nullable=False, default=0),
    )

    # Step 2: Copy data from `player` to `player_temp`
    op.execute("INSERT INTO player_temp (id, user_id, title, level, experience) SELECT id, user_id, title, level, experience FROM player")

    # Step 3: Drop the old `player` table
    op.drop_table("player")

    # Step 4: Rename `player_temp` to `player`
    op.rename_table("player_temp", "player")


def downgrade():
    # Step 1: Recreate original `player` table (without CASCADE)
    op.create_table(
        "player_old",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False, unique=True),
        sa.Column("title", sa.String, nullable=False, default="Noobie"),
        sa.Column("level", sa.Integer, nullable=False, default=1),
        sa.Column("experience", sa.Integer, nullable=False, default=0),
    )

    # Step 2: Copy data back from `player` to `player_old`
    op.execute("INSERT INTO player_old (id, user_id, title, level, experience) SELECT id, user_id, title, level, experience FROM player")

    # Step 3: Drop the modified `player` table
    op.drop_table("player")

    # Step 4: Rename `player_old` back to `player`
    op.rename_table("player_old", "player")
