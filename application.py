import os
import sys
from app import create_app
from flask_script import Manager
from app import db
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# manager = Manager(app)

if __name__ == '__main__':
    # manager.run()
    app.run()
