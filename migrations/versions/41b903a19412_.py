"""empty message

Revision ID: 41b903a19412
Revises: b1181a3ac9cb
Create Date: 2024-05-13 22:10:55.602084

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '41b903a19412'
down_revision: Union[str, None] = 'b1181a3ac9cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pictures', 'og_picture_path')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pictures', sa.Column('og_picture_path', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
