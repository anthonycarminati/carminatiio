from flask import Flask, session
from config import config
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from flask.ext.moment import Moment
from flask.ext.mail import Mail
from datetime import timedelta
from flask.ext.misaka import Misaka

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
db = SQLAlchemy()
pagedown = PageDown()
moment = Moment()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    Misaka(app)

    from .site import site as site_blueprint
    app.register_blueprint(site_blueprint)

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
