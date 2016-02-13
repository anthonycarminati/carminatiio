from flask import render_template, request, redirect, url_for, flash, abort, g, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from ..models import User
from forms import LoginForm, NewUser
from . import auth
from app import db
from flask.ext.mail import Message
from app import mail
from itsdangerous import URLSafeTimedSerializer
import app
import os
from .util import ts


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password.')
            return redirect(url_for('.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully.')
        return redirect(url_for('site.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return render_template('auth/logout.html')


@auth.route('/register', methods=['GET', 'POST'])
def create_account():
    form = NewUser()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).order_by(User.member_since.desc()).first():
            flash('Email already registered!')
        else:
            # CREATE USER
            user = User(email=form.email.data,
                        password=form.email.data,
                        username=form.email.data,
                        name=form.first_name.data + " " + form.last_name.data)
            db.session.add(user)
            db.session.commit()
            # GET SECURITY TOKEN
            token = ts.dumps(form.email.data, salt='email-confirm-key')
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            # WRITE CONFIRMATION EMAIL AND SEND
            msg = Message(subject='Registration Confirmation for carminati.io!',
                          sender='noreply@carminati.io',
                          recipients=[form.email.data])
            msg.body = """
                  Hey {first_name},

                  Thanks for registering for my site! Please confirm your email with the link below:

                  {confirm}

                  -Anthony

                  """.format(first_name=form.first_name.data, confirm=confirm_url)
            mail.send(msg)
            flash('Confirmation email sent!')
            return redirect(url_for('site.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    try:
        email = ts.loads(token, salt='email-confirm-key', max_age=86400)
        form = LoginForm()
    except:
        abort(404)

    user = User.query.filter_by(email=email).order_by(User.member_since.desc()).first_or_404()

    user.is_confirmed = True

    db.session.add(user)
    db.session.commit()

    return render_template('auth/login.html', form=form)
