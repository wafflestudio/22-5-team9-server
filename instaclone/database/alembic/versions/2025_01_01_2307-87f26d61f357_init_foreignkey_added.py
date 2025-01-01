"""init_foreignkey_added

Revision ID: 87f26d61f357
Revises: 68f5f925c123
Create Date: 2025-01-01 23:07:43.458130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87f26d61f357'
down_revision: Union[str, None] = '68f5f925c123'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'comments', 'comments', ['parent_id'], ['comment_id'])
    op.create_foreign_key(None, 'comments', 'users', ['user_id'], ['user_id'])
    op.create_foreign_key(None, 'followers', 'users', ['follower_id'], ['user_id'])
    op.create_foreign_key(None, 'followers', 'users', ['following_id'], ['user_id'])
    op.create_foreign_key(None, 'media', 'posts', ['post_id'], ['post_id'])
    op.create_foreign_key(None, 'media', 'stories', ['story_id'], ['story_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'media', type_='foreignkey')
    op.drop_constraint(None, 'media', type_='foreignkey')
    op.drop_constraint(None, 'followers', type_='foreignkey')
    op.drop_constraint(None, 'followers', type_='foreignkey')
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_constraint(None, 'comments', type_='foreignkey')
    # ### end Alembic commands ###
