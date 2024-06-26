"""init

Revision ID: dcbe7000f233
Revises: e0cbc518e18d
Create Date: 2024-04-08 17:59:35.474881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision: str = 'dcbe7000f233'
down_revision: Union[str, None] = 'e0cbc518e18d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('translationrequest', sa.Column('token_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('translationrequest', 'token_count')
    # ### end Alembic commands ###
