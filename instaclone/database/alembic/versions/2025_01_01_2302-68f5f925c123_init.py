"""init

Revision ID: 68f5f925c123
Revises: 
Create Date: 2025-01-01 23:02:46.330101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68f5f925c123'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('post_id', sa.BigInteger(), nullable=False),
    sa.Column('comment_id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('parent_id', sa.BigInteger(), nullable=True),
    sa.Column('comment_text', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('comment_id')
    )
    op.create_table('followers',
    sa.Column('follower_id', sa.BigInteger(), nullable=False),
    sa.Column('following_id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('follower_id', 'following_id')
    )
    op.create_table('media',
    sa.Column('post_id', sa.BigInteger(), nullable=True),
    sa.Column('story_id', sa.BigInteger(), nullable=True),
    sa.Column('image_id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('file_name', sa.String(length=100), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('image_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('full_name', sa.String(length=4), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=11), nullable=False),
    sa.Column('creation_date', sa.Date(), nullable=False),
    sa.Column('profile_image', sa.String(length=100), nullable=False),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=False),
    sa.Column('introduce', sa.String(length=100), nullable=False),
    sa.Column('website', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number'),
    sa.UniqueConstraint('username')
    )
    op.create_table('posts',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('post_id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('location', sa.String(length=50), nullable=True),
    sa.Column('post_text', sa.String(length=500), nullable=True),
    sa.Column('creation_date', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_table('stories',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('story_id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('creation_date', sa.DATETIME(), nullable=False),
    sa.Column('expiration_date', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('story_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stories')
    op.drop_table('posts')
    op.drop_table('users')
    op.drop_table('media')
    op.drop_table('followers')
    op.drop_table('comments')
    # ### end Alembic commands ###
