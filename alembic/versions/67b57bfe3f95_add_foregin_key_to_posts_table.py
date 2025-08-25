"""add foregin-key to posts table

Revision ID: 67b57bfe3f95
Revises: 2a98c86ceaa7
Create Date: 2025-08-25 22:26:01.563741

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "67b57bfe3f95"
down_revision: Union[str, Sequence[str], None] = "2a98c86ceaa7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
