"""empty message

Revision ID: 889400379e85
Revises: 34971689d3dc
Create Date: 2024-05-02 21:57:46.844674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '889400379e85'
down_revision: Union[str, None] = '34971689d3dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('age_rating_games_game_id_fkey', 'age_rating_games', type_='foreignkey')
    op.create_foreign_key(None, 'age_rating_games', 'games', ['game_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('game_platforms_game_id_fkey', 'game_platforms', type_='foreignkey')
    op.create_foreign_key(None, 'game_platforms', 'games', ['game_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'game_platforms', type_='foreignkey')
    op.create_foreign_key('game_platforms_game_id_fkey', 'game_platforms', 'games', ['game_id'], ['id'])
    op.drop_constraint(None, 'age_rating_games', type_='foreignkey')
    op.create_foreign_key('age_rating_games_game_id_fkey', 'age_rating_games', 'games', ['game_id'], ['id'])
    # ### end Alembic commands ###
