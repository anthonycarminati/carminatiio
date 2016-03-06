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
        'blog_comment'
    )
    op.create_table(
        'blog_post'
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
        'blog_followers'
    )


def downgrade():
    pass
