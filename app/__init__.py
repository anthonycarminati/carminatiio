from flask import Flask
from config import config
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

login_manager = LoginManager()

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .site import site as site_blueprint
    app.register_blueprint(site_blueprint)

    return app
