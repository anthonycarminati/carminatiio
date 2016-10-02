import os
import sys
from application import create_app
from flask.ext.script import Manager
from application import db
from application.models import User

application = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(application)

@manager.command
def adduser(first_name, last_name, email, username, admin=False):
    """Register a new user."""
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        sys.exit('Error: passwords do not match.')
    if username in password:
        sys.exit('Error: password cannot contain username.')
    db.create_all()
    user = User(name=first_name+" "+last_name,
                email=email,
                username=username,
                password=password,
                is_admin=admin)
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered successfully.'.format(username))

if __name__ == '__main__':
    manager.run()
