"""empty message

Revision ID: 0db792cd0342
Revises: e9ba5393b51b
Create Date: 2024-02-25 20:12:38.396497

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0db792cd0342'
down_revision: str | None = 'e9ba5393b51b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('list_games_list_id_fkey', 'list_games', type_='foreignkey')
    op.create_foreign_key(None, 'list_games', 'playlists', ['list_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'list_games', type_='foreignkey')
    op.create_foreign_key('list_games_list_id_fkey', 'list_games', 'user_lists', ['list_id'], ['id'])
    # ### end Alembic commands ###
