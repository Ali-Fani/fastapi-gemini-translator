"""init

Revision ID: 727d5174b54f
Revises: 4949dd9bbdf9
Create Date: 2024-04-08 17:42:59.027038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision: str = '727d5174b54f'
down_revision: Union[str, None] = '4949dd9bbdf9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
