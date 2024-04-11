"""init

Revision ID: fa8aad988b80
Revises: 
Create Date: 2024-04-07 19:53:39.255919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision: str = 'fa8aad988b80'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('song',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('artist', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('translationrequest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rich_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('source_language', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('target_language', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('translated_text', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('callback_url', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('request_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('retries', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('request_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('translationrequest')
    op.drop_table('song')
    # ### end Alembic commands ###