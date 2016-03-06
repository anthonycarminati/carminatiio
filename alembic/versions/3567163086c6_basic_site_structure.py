"""basic site structure

Revision ID: 3567163086c6
Revises: 
Create Date: 2016-03-05 18:19:19.127983

"""

# revision identifiers, used by Alembic.
revision = '3567163086c6'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from datetime import datetime


def upgrade():
    op.create_table(
        'blog_comment',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('body', sa.Text),
        sa.Column('comment_date', sa.DateTime, index=True, default=datetime.utcnow()),
        sa.Column('commenter_id', sa.Integer, sa.ForeignKey('blog_user.id')),
        sa.Column('notify', sa.Boolean),
        sa.Column('approved', sa.Boolean),
        sa.Column('post_id', sa.Integer, sa.ForeignKey('blog_post.id'))
    )
    op.create_table(
        'blog_post',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('blog_user.id')),
        sa.Column('title', sa.String(255)),
        sa.Column('subtitle', sa.String(255)),
        sa.Column('body', sa.Text),
        sa.Column('post_date', sa.DateTime, index=True, default=datetime.utcnow())

    )
    op.create_table(
        'blog_user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(64), index=True, unique=True),
        sa.Column('username', sa.String(64), index=True, unique=True),
        sa.Column('is_admin', sa.Boolean),
        sa.Column('password_hash', sa.String(256)),
        sa.Column('name', sa.String(64)),
        sa.Column('location', sa.String(64)),
        sa.Column('bio', sa.Text()),
        sa.Column('member_since', sa.DateTime(), default=datetime.utcnow()),
        sa.Column('avatar_hash', sa.String(64)),
        sa.Column('remember_me', sa.Boolean),
        sa.Column('is_confirmed', sa.Boolean)
    )
    op.create_table(
        'blog_follower',
        sa.Column('follower_id', sa.Integer, sa.ForeignKey('blog_user.id')),
        sa.Column('followed_id', sa.Integer, sa.ForeignKey('blog_user.id'))
    )


def downgrade():
    op.drop_table('blog_comment')
    op.drop_table('blog_post')
    op.drop_table('blog_user')
    op.drop_table('blog_follower')
