"""add column is_admin table user

Revision ID: 42e09510bc62
Revises: e8dd3a554661
Create Date: 2025-03-04 20:31:31.966626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42e09510bc62'
down_revision: Union[str, None] = 'e8dd3a554661'
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
