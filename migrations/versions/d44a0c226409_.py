"""empty message

Revision ID: d44a0c226409
Revises: 6279c3dfad70
Create Date: 2024-01-23 20:50:32.580836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd44a0c226409'
down_revision: Union[str, None] = '6279c3dfad70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'disabled')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('disabled', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###