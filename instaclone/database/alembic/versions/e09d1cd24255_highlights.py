"""Highlights

Revision ID: e09d1cd24255
Revises: d9846c7e8030
Create Date: 2025-01-21 14:43:17.693479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e09d1cd24255'
down_revision: Union[str, None] = 'd9846c7e8030'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_likes',
    sa.Column('like_id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('content_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['content_id'], ['posts.post_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('like_id')
    )
    op.create_table('story_likes',
    sa.Column('like_id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('content_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['content_id'], ['stories.story_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('like_id')
    )
    op.create_table('comment_likes',
    sa.Column('like_id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('content_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['content_id'], ['comments.comment_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('like_id')
    )
    op.create_table('highlights',
    sa.Column('highlight_id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('highlight_name', sa.String(length=15), nullable=False),
    sa.Column('cover_image_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['cover_image_id'], ['media.image_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('highlight_id')
    )
    op.create_table('highlight_stories',
    sa.Column('highlight_id', sa.BigInteger(), nullable=False),
    sa.Column('story_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['highlight_id'], ['highlights.highlight_id'], ),
    sa.ForeignKeyConstraint(['story_id'], ['stories.story_id'], ),
    sa.PrimaryKeyConstraint('highlight_id', 'story_id')
    )
    op.add_column('followers', sa.Column('created_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('followers', 'created_at')
    op.drop_table('highlight_stories')
    op.drop_table('highlights')
    op.drop_table('comment_likes')
    op.drop_table('story_likes')
    op.drop_table('post_likes')
    # ### end Alembic commands ###
