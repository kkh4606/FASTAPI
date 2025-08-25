"""add content column

Revision ID: 1dd0c4987050
Revises: 163bb666f171
Create Date: 2025-08-25 21:39:29.178061

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1dd0c4987050"
down_revision: Union[str, Sequence[str], None] = "163bb666f171"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("posts", "content")
    pass
