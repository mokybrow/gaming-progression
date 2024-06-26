"""empty message

Revision ID: a1967e6ac62c
Revises: 
Create Date: 2024-05-06 13:14:45.146692

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a1967e6ac62c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'playlist_games',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('game_id', sa.Uuid(), nullable=False),
        sa.Column('list_id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.ForeignKeyConstraint(
            ['game_id'],
            ['games.id'],
        ),
        sa.ForeignKeyConstraint(
            ['list_id'],
            ['playlists.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('game_id', 'list_id', name='_game_list_uc'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('playlist_games')
    # ### end Alembic commands ###
