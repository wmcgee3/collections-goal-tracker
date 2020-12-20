from getpass import getpass

from flask_bcrypt import generate_password_hash

from goal_tracker import db, create_app
from goal_tracker.models import User, Month

app = create_app()
db.create_all(app=create_app())

with app.app_context():

    months = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }

    for name, number in months.items():
        new_month = Month(
            name=name,
            number=number
        )
        db.session.add(new_month)

    another_user = 'y'

    while another_user.lower() == 'y' or another_user.lower() == 'yes':
        username = input('Username: ')
        password = getpass()

        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)

        another_user = input('Would you like to add another user? (y/N): ')

    db.session.commit()
