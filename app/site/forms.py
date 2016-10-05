from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Email
from wtforms.fields.html5 import DateField
from wtforms import validators


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired('Please enter a subject')])
    email = StringField("Email Address", validators=[DataRequired('Please enter a subject'), Email()])
    subject = StringField("Subject", validators=[DataRequired('Please enter a subject'), Length(min=0, max=140)])
    message = TextAreaField("Message", validators=[DataRequired('Please enter a message')])
    submit = SubmitField("Send")