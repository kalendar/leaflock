"""Add licenses to topics and activities.

Revision ID: 055ce6e4083c
Revises: 7fd433c8e65b
Create Date: 2025-04-21 15:27:58.233452

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "055ce6e4083c"
down_revision: Union[str, None] = "7fd433c8e65b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("activities", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "license",
                sa.Enum(
                    "CC0_1_0",
                    "CC_BY_4_0",
                    "CC_BY_SA_4_0",
                    "CC_BY_NC_4_0",
                    "CC_BY_NC_SA_4_0",
                    name="license",
                ),
                nullable=False,
                server_default="CC0_1_0",
            )
        )

    with op.batch_alter_table("topics", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "license",
                sa.Enum(
                    "CC0_1_0",
                    "CC_BY_4_0",
                    "CC_BY_SA_4_0",
                    "CC_BY_NC_4_0",
                    "CC_BY_NC_SA_4_0",
                    name="license",
                ),
                nullable=False,
                server_default="CC0_1_0",
            )
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("topics", schema=None) as batch_op:
        batch_op.drop_column("license")

    with op.batch_alter_table("activities", schema=None) as batch_op:
        batch_op.drop_column("license")
    # ### end Alembic commands ###
