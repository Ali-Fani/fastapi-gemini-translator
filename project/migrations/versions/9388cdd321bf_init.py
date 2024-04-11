"""init

Revision ID: 9388cdd321bf
Revises: fa8aad988b80
Create Date: 2024-04-07 20:34:31.216233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision: str = '9388cdd321bf'
down_revision: Union[str, None] = 'fa8aad988b80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('song')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('song',
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('artist', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='song_pkey')
    )
    # ### end Alembic commands ###