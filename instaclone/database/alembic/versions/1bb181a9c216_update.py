"""update

Revision ID: 1bb181a9c216
Revises: e5c3b8991c39
Create Date: 2025-01-28 15:40:11.625754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bb181a9c216'
down_revision: Union[str, None] = 'e5c3b8991c39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location_tags',
    sa.Column('location_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('citation_count', sa.Integer(), server_default='0', nullable=False),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('location_id')
    )
    op.create_index(op.f('ix_location_tags_location_id'), 'location_tags', ['location_id'], unique=False)
    op.add_column('users', sa.Column('location_status', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('location_expired_at', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'users', 'location_tags', ['location_status'], ['location_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'location_expired_at')
    op.drop_column('users', 'location_status')
    op.drop_index(op.f('ix_location_tags_location_id'), table_name='location_tags')
    op.drop_table('location_tags')
    # ### end Alembic commands ###
