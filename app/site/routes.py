from flask import render_template, request, flash, redirect, url_for
from . import site
from .forms import ContactForm
from app import mail
from flask.ext.mail import Message
from ..models import Post


@site.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    # post = Post.query.order_by(Post.post_date.desc()).first()

    if request.method == 'GET':
        return render_template('site/index.html', form=form)
    elif request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('site/index.html', form=form)
        elif form.validate():
            msg = Message(form.subject.data, sender='noreply@carminati.io', recipients=['anthony@carminati.io'])
            msg.body = """
              From: {name}
              Email Address: {email}
              Message: {message}
              """.format(name=form.name.data, email=form.email.data, message=form.message.data)
            mail.send(msg)
        form = ContactForm()
        return redirect(url_for('.index'), form=form)


# @site.route('/contact', methods=['GET', 'POST'])
# def contact():
#     form = ContactForm()
#
#     if request.method == 'GET':
#         return render_template('site/contact.html', form=form)
#     elif request.method == 'POST':
#         if form.validate() == False:
#             flash('All fields are required.')
#             return render_template('site/contact.html', form=form)
#         elif form.validate() == True:
#             msg = Message(form.subject.data, sender='noreply@carminati.io', recipients=['anthony@carminati.io'])
#             msg.body = """
#               From: {name}
#               Email Address: {email}
#               Message: {message}
#               """.format(name=form.name.data, email=form.email.data, message=form.message.data)
#             mail.send(msg)
#         return redirect(url_for('.contact'))
