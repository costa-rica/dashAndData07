from flask import Flask
from app_package.config import config
import os
import logging
from logging.handlers import RotatingFileHandler
from pytz import timezone
from datetime import datetime
from dd07_models import login_manager
from flask_mail import Mail


if not os.path.exists(os.path.join(os.environ.get('WEB_ROOT'),'logs')):
    os.makedirs(os.path.join(os.environ.get('WEB_ROOT'), 'logs'))

# timezone 
def timetz(*args):
    return datetime.now(timezone('Europe/Paris') ).timetuple()

logging.Formatter.converter = timetz

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
formatter_terminal = logging.Formatter('%(asctime)s:%(filename)s:%(name)s:%(message)s')

logger_init = logging.getLogger('__init__')
logger_init.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler(os.path.join(os.environ.get('WEB_ROOT'),'logs','__init__.log'), mode='a', maxBytes=5*1024*1024,backupCount=2)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter_terminal)

stream_handler_tz = logging.StreamHandler()

logger_init.addHandler(file_handler)
logger_init.addHandler(stream_handler)

logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('werkzeug').addHandler(file_handler)

logger_init.info(f'--- Starting Dashboards and Databases 07 web application---')
TEMPORARILY_DOWN = "ACTIVE" if os.environ.get('TEMPORARILY_DOWN') == "1" else "inactive"
logger_init.info(f"- TEMPORARILY_DOWN: {TEMPORARILY_DOWN}")
logger_init.info(f"- SQL_URI_USERS: sqlite:///{os.environ.get('DB_ROOT')}{os.environ.get('DB_NAME_USERS')}")

mail = Mail()

def create_app(config_for_flask = config):
    app = Flask(__name__)   
    app.config.from_object(config_for_flask)
    login_manager.init_app(app)
    mail.init_app(app)

    from app_package.bp_main.routes import bp_main
    from app_package.bp_users.routes import bp_users
    from app_package.bp_admin.routes import bp_admin
    from app_package.bp_error.routes import bp_error

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_error)

    return app