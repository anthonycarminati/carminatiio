from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Email
from wtforms.fields.html5 import DateField
from flask.ext.pagedown.fields import PageDownField


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])


class ProfileForm(Form):
    name = StringField('Name', validators=[Optional(), Length(1, 64)])
    location = StringField('Location', validators=[Optional(), Length(1, 64)])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    body = TextAreaField('Body')
    date = DateField('Date')

    def from_model(self, post):
        self.title.data = post.title
        self.body.data = post.body
        self.date.data = post.date

    def to_model(self, post):
        post.title = self.title.data
        post.body = self.body.data
        post.date = self.date.data


class AdminCommentForm(Form):
    body = PageDownField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired, Length(1, 64), Email()])
    body = PageDownField('Comment', validators=[DataRequired()])
    notify = BooleanField('Notify when new comments are posted', default=True)
    submit = SubmitField('Submit')
