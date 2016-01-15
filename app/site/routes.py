from flask import render_template, request, flash
from . import site
from .forms import ContactForm
from app import mail
from flask.ext.mail import Message


@site.route('/')
def index():
    return render_template('site/index.html')

@site.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'GET':
        return render_template('site/contact.html', form=form)
    elif request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('site/contact.html', form=form)
        elif form.validate() == True:
            msg = Message(form.subject.data, sender='noreply@carminati.io', recipients=['anthony@carminati.io'])
            msg.body = 'test'
            msg.body = """
              From: {0} <{1}>
              {2}
              """.format(form.name.data, form.email.data, form.message.data)
            mail.send(msg)

    return render_template('site/contact.html')
