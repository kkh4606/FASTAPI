"""add last few columns to post table

Revision ID: 30fef2bdb49b
Revises: 67b57bfe3f95
Create Date: 2025-08-25 22:38:32.244597

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "30fef2bdb49b"
down_revision: Union[str, Sequence[str], None] = "67b57bfe3f95"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )

    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
