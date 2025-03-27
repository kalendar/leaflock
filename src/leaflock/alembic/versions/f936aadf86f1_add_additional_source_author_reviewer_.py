"""Add additional source/author/reviewer columns

Revision ID: f936aadf86f1
Revises: a034d08cbfd1
Create Date: 2025-03-27 14:16:57.781232

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f936aadf86f1"
down_revision: Union[str, None] = "a034d08cbfd1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("activities", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("sources", sa.String(), nullable=False, default="")
        )
        batch_op.add_column(
            sa.Column("authors", sa.String(), nullable=False, default="")
        )

    with op.batch_alter_table("textbooks", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("reviewers", sa.String(), nullable=False, default="")
        )

    with op.batch_alter_table("topics", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("sources", sa.String(), nullable=False, default="")
        )
        batch_op.add_column(
            sa.Column("authors", sa.String(), nullable=False, default="")
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("topics", schema=None) as batch_op:
        batch_op.drop_column("authors")
        batch_op.drop_column("sources")

    with op.batch_alter_table("textbooks", schema=None) as batch_op:
        batch_op.drop_column("reviewers")

    with op.batch_alter_table("activities", schema=None) as batch_op:
        batch_op.drop_column("authors")
        batch_op.drop_column("sources")

    # ### end Alembic commands ###
