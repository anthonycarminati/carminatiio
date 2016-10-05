from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Email
from wtforms.fields.html5 import DateField
from flask_pagedown.fields import PageDownField
import datetime


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])


class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[Optional(), Length(1, 64)])
    location = StringField('Location', validators=[Optional(), Length(1, 64)])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 255)])
    subtitle = StringField('Sub-Title', validators=[DataRequired(), Length(1, 255)])
    body = TextAreaField('Body')
    # date = DateField('Date')
    submit = SubmitField('Submit')

    def from_model(self, post):
        self.title.data = post.title
        self.subtitle.data = post.subtitle
        self.body.data = post.body
        self.date.data = post.date

    def to_model(self, post):
        post.title = self.title.data
        post.subtitle = self.subtitle.data
        post.body = self.body.data
        post.date = datetime.datetime.now()


class AdminCommentForm(FlaskForm):
    body = PageDownField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired, Length(1, 64), Email()])
    body = PageDownField('Comment', validators=[DataRequired()])
    notify = BooleanField('Notify when new comments are posted', default=True)
    submit = SubmitField('Submit')
