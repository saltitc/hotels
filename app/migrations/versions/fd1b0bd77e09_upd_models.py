"""Upd models

Revision ID: fd1b0bd77e09
Revises: a5b47857e4fb
Create Date: 2023-12-09 15:27:42.596905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd1b0bd77e09'
down_revision: Union[str, None] = 'a5b47857e4fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'hotel_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('rooms', 'hotel_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###