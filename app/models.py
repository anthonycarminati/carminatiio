import hashlib
import bleach
import config
from datetime import datetime
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import request, current_app
from flask.ext.login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from app import db, login_manager

def db_connect():
    return create_engine(URL(**config['SQLALCHEMY_DATABASE_URI']))

followers = db.Table(
        'blog_followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('blog_user.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('blog_user.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'blog_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(256))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    bio = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow())
    avatar_hash = db.Column(db.String(64))
    remember_me = db.Column(db.Boolean)
    is_confirmed = db.Column(db.Boolean)

    post = db.relationship('Post', lazy='dynamic', backref='author')
    comment = db.relationship('Comment', lazy='dynamic', backref='author')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<User {user}>'.format(user=self.username)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_api_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('id')
        if id:
            return User.query.get(id)
        return None

    def get_api_token(self, expiration=300):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'user': self.id}).decode('utf-8')

    # def gravatar(self, size=100, default='identicon', rating='g'):
    #     if request.is_secure:
    #         url = 'https://secure.gravatar.com/avatar'
    #     else:
    #         url = 'http://www.gravatar.com/avatar'
    #     grav_hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
    #     return '{url}/{grav_hash}?s={size}&d={default}&r={rating}'.\
    #         format(url=url, hash=grav_hash, size=size, default=default, rating=rating)
    # ---------------
    # For following posts and users
    # ---------------
    # def follow(self, user):
    #     if not self.is_following(user):
    #         self.followed.append(user)
    #         return self
    # def unfollow(self, user):
    #     if self.is_following(user):
    #         self.followed.remove(user)
    #         return self
    # def is_following(self, user):
    #     return self.followed.filter(blog_followers.c.followed_id == user.id).count() > 0
    # def followed_posts(self):
    #     return Post.query.join(blog_followers, (blog_followers.c.followed_id == Post.id)).filter(
    #         blog_followers.c.follower_id == self.id).order_by(Post.timestamp.desc())
    # def for_moderation(self, admin=False):
    #     if admin and self.is_admin:
    #         return Comment.for_moderation()
    #     return Comment.query.join(Post, Comment.post_id == Post.id).\
    #     filter(Talk.author == self).filter(Comment.approved == False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('blog_user.id'))
    title = db.Column(db.String(255))
    subtitle = db.Column(db.String(255))
    body = db.Column(db.Text)
    post_date = db.Column(db.DateTime, index=True, default=datetime.utcnow())


    def __repr__(self):
        return '<Post {body}>'.format(body=self.body)


class Comment(db.Model):
    __tablename__ = 'blog_comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    comment_date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    commenter_id = db.Column(db.Integer, db.ForeignKey('blog_user.id'))
    notify = db.Column(db.Boolean)
    approved = db.Column(db.Boolean)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify\
        (bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))

    @staticmethod
    def for_moderation():
        return Comment.query.filter(Comment.approved == False)

    def notification_list(self):
        notify_list = {}
        for comment in self.blog.comment:
            # include all commenters that have notifications enabled except
            # the author of the talk and the author of this comment
            if comment.notify and comment.author != comment.blog.author:
                if comment.author:
                    # REGISTERED USERS
                    if self.author != comment.author:
                        notify_list[comment.author.email] = comment.author.name or comment.author.username
                else:
                    # REGULAR USERS
                    if self.author_email != comment.author_email:
                        notify_list[comment.author_email] = comment.author_name
        return notify_list.items()


# db.event.listen(Comment.body, 'set', Comment.on_changed_body)


# class PendingEmail(db.Model):
#     __tablename__ = 'blog_pending_emails'
#     email_id
#     name
#     email
#     subject
#     body_text
#     body_html
#     talk_id
#     timestamp
#
#     @staticmethod
#     def already_in_queue(email, talk):