"""empty message

Revision ID: d49031133247
Revises: b44fa6e3d8c1
Create Date: 2024-04-17 16:03:31.739377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd49031133247'
down_revision: Union[str, None] = 'b44fa6e3d8c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'comments_count')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('comments_count', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
