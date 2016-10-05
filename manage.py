import os
import sys
from app import create_app
from flask_script import Manager
from app import db
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

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
