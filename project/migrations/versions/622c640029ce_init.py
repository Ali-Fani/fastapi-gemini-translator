"""init

Revision ID: 622c640029ce
Revises: a8cf288e64c3
Create Date: 2024-04-07 21:36:47.057003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '622c640029ce'
down_revision: Union[str, None] = 'a8cf288e64c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('translationrequest', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('translationrequest', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    # ### end Alembic commands ###
