"""empty message

Revision ID: 70961c9aa4c1
Revises: 7517b761f178
Create Date: 2024-02-27 22:26:33.604247

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '70961c9aa4c1'
down_revision: Union[str, None] = '7517b761f178'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_user_mailing_uc', 'user_mailings', ['user_id', 'mailing_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_user_mailing_uc', 'user_mailings', type_='unique')
    # ### end Alembic commands ###
