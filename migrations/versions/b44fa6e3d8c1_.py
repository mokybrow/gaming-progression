"""empty message

Revision ID: b44fa6e3d8c1
Revises: db2ac1d56959
Create Date: 2024-04-17 13:19:20.484364

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b44fa6e3d8c1'
down_revision: Union[str, None] = 'db2ac1d56959'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('likes_count', sa.Integer(), nullable=False))
    op.add_column('posts', sa.Column('comments_count', sa.Integer(), nullable=False))
    op.drop_column('posts', 'like_count')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('like_count', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('posts', 'comments_count')
    op.drop_column('posts', 'likes_count')
    # ### end Alembic commands ###