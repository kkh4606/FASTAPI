"""add user table

Revision ID: 2a98c86ceaa7
Revises: 1dd0c4987050
Create Date: 2025-08-25 21:57:54.044213

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2a98c86ceaa7"
down_revision: Union[str, Sequence[str], None] = "1dd0c4987050"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("users")
    pass
