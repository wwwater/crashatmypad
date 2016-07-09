from datetime import date

from flask_mail import Message

from crashatmypad import logger, mail, db

from crashatmypad.persistence.user import User
from crashatmypad.persistence.password import Password


def get_user_by_id(user_id):
    return db.session.query(User).get(user_id)


def find_user_by_email(email):
    return User.query.filter_by(email=email).first()


def find_user_password_by_email(email):
    return Password.query.filter_by(username=email).first()


def send_confirmation_email(user):
    message_body = \
        'Hi {}!<br/><br/>' \
        'We\'re glad you registered on ' \
        '<span style="color:green">Crash at my Pad</span> : )<br/>' \
        'Please follow the ' \
        '<a href="https://atmypad.com/user/{}?confirm={}">' \
        'link to confirm your email</a>.<br/><br/>' \
        'Have a nice day!<br/>' \
        'Your CrashAtMyPad team'.format(
            (user.name or _get_first_name_from_email(user.email)),
            user.id,
            user.confirmation_hash)
    message = Message("Please confirm your email on Crash At My Pad",
                      recipients=[user.email],
                      html=message_body)

    mail.send(message)


def confirm_email(user, confirmation_hash):
    if confirmation_hash == user.confirmation_hash:
        logger.info('User email %s is confirmed', user.email)
        user.email_is_confirmed = True
        db.session.commit()
        return True
    else:
        logger.warn('User %s tried to use wrong confirmation hash',
                        user.email)
        return False


def get_user_data_to_display(user):
    if user.birthday:
        today = date.today()
        diff_pure_years = today.year - user.birthday.year
        age = diff_pure_years \
            if user.birthday.replace(today.year) <= today \
            else diff_pure_years - 1
    else:
        age = 21
    user_data_to_display = {
        'name': user.name,
        'last_name': user.last_name,
        'age': age,
        'profession': user.profession
    }

    locations = user.locations
    locations_to_display = []
    for location in locations:
        location_to_display = {
            'country': location.country,
            'city': location.city,
            'apartment': location.apartment,
            'room': location.room,
            'corner': location.corner,
            'yard': location.yard,
            'trees': location.trees,
            'driveway': location.driveway,
            'shower': location.shower,
            'bathroom': location.bathroom
        }
        locations_to_display.append(location_to_display)
    return user_data_to_display, locations_to_display


def create_new_user(username, password):
    user = User(email=username)
    password_entry = Password(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    db.session.add(password_entry)
    db.session.commit()
    send_confirmation_email(user)
    return user


def _get_first_name_from_email(email):
    return email.split('@')[0].split('.')[0]
