from flask import Flask
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler


app = Flask(__name__, instance_relative_config=False)

app.config.from_object('config.settings')
app.config.from_pyfile('../config/settings.py', silent=False)
app.logger.setLevel(logging.INFO)

# log to stream
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
app.logger.addHandler(stream_handler)

# log to file
file_handler = RotatingFileHandler(
    'app_logging.log',
    maxBytes=10000,
    backupCount=1)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
app.logger.addHandler(file_handler)

# log to email
if app.config['ENV'] is 'production':
    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], 587),
        fromaddr=app.config['MAIL_NO_REPLY_SENDER'],
        toaddrs=app.config['MAIL_USERNAME'],
        subject='ERROR on CrashAtMyPad',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
        secure=())
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    app.logger.addHandler(mail_handler)


