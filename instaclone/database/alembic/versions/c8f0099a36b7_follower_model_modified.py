"""follower model modified

Revision ID: c8f0099a36b7
Revises: 41185fea0a70
Create Date: 2025-01-10 15:36:10.848746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8f0099a36b7'
down_revision: Union[str, None] = '41185fea0a70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blocked_token',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('jti', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('followers', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.drop_constraint('media_ibfk_2', 'media', type_='foreignkey')
    op.create_foreign_key(None, 'media', 'stories', ['story_id'], ['story_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'media', type_='foreignkey')
    op.create_foreign_key('media_ibfk_2', 'media', 'stories', ['story_id'], ['story_id'])
    op.drop_column('followers', 'created_at')
    op.drop_table('blocked_token')
    # ### end Alembic commands ###
