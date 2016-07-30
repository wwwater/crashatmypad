import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import settings


app = Flask(__name__, instance_relative_config=False)

# global variables that are imported from other places in the app
login_manager = LoginManager()
mail = Mail()
db = SQLAlchemy()
logger = app.logger
config = app.config


def create_app(environment):

    if environment is 'DEVELOPMENT':
        app.config.from_object(settings.LocalDevelopmentConfig)
    elif environment is 'TESTING':
        app.config.from_object(settings.TestingConfig)
    elif environment is 'PRODUCTION':
        app.config.from_object(settings.ProductionConfig)
    else:
        raise EnvironmentError('No environment specified!')

    logger.setLevel(logging.INFO)

    # log to stream
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    logger.addHandler(stream_handler)

    # log to file
    file_handler = RotatingFileHandler(
        'app_logging.log',
        maxBytes=10000,
        backupCount=1)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    logger.addHandler(file_handler)

    # log to email
    if environment is 'PRODUCTION':
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], 587),
            fromaddr=app.config['MAIL_NO_REPLY_SENDER'],
            toaddrs=app.config['MAIL_USERNAME'],
            subject='ERROR on CrashAtMyPad',
            credentials=(app.config['MAIL_USERNAME'],
                         app.config['MAIL_PASSWORD']),
            secure=())
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
        logger.addHandler(mail_handler)

    from crashatmypad.create_api import create_api
    db.init_app(app)
    db.create_all(app=app)  # creates new tables but doesn't overwrite existing

    create_api(app)

    login_manager.init_app(app)
    mail.init_app(app)

    logger.info('App has been created!')

    return app

