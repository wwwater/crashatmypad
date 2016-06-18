from flask_mail import Mail, Message

from crashatmypad.persistence.db import db

mail = Mail()


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
        print 'Confirming email'
        user.email_is_confirmed = True
        db.session.commit()
        return True
    else:
        print 'Confirmation hash is wrong'
        return False


def _get_first_name_from_email(email):
    return email.split('@')[0].split('.')[0]
