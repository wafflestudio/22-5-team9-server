"""Increase full_name column length

Revision ID: 18e806f94e68
Revises: 87f26d61f357
Create Date: 2025-01-03 17:43:37.091907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '18e806f94e68'
down_revision: Union[str, None] = '87f26d61f357'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'full_name',
               existing_type=mysql.VARCHAR(length=4),
               type_=sa.String(length=30),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'full_name',
               existing_type=sa.String(length=30),
               type_=mysql.VARCHAR(length=4),
               existing_nullable=False)
    # ### end Alembic commands ###
