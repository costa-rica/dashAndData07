from flask import Flask
from app_package.config import config
import os
import logging
from logging.handlers import RotatingFileHandler
from pytz import timezone
from datetime import datetime
# from dd07_models import login_manager
from dd07_models import login_manager, dict_sess, \
    dict_engine, text, dict_base, \
    Users, BlogPosts, CageCompanies, IndustryNames, \
    IndustryValues, CommodityNames, CommodityValues
from flask_mail import Mail
import secure

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
logger_init.info(f"- FLASK_CONFIG_TYPE: {os.environ.get('FLASK_CONFIG_TYPE')}")

mail = Mail()
secure_headers = secure.Secure()

def create_app(config_for_flask = config):
    app = Flask(__name__)   
    app.config.from_object(config_for_flask)
    login_manager.init_app(app)
    mail.init_app(app)

    logger_init.info(f"- DB_ROOT: {config_for_flask.DB_ROOT}")
    # logger_init.info(f"- ENV: {app.config['ENV']}")


    ############################################################################
    ## Build Auxiliary directories in DB_ROOT
    if not os.path.exists(config_for_flask.DB_ROOT):
        os.makedirs(config_for_flask.DB_ROOT)
    # # config.DIR_DB_AUXILARY directory:
    # if not os.path.exists(os.path.join(config_for_flask.DB_ROOT,"auxilary")):
    #     os.makedirs(os.path.join(config_for_flask.DB_ROOT,"auxilary"))
    # # config.DIR_DB_AUX_IMAGES_PEOPLE directory:
    # if not os.path.exists(os.path.join(config_for_flask.DB_ROOT,"auxilary","images_people")):
    #     os.makedirs(os.path.join(config_for_flask.DB_ROOT,"auxilary","images_people"))
    # # config.DIR_DB_AUX_BLOG directory:
    # if not os.path.exists(os.path.join(config_for_flask.DB_ROOT,"auxilary","blog")):
    #     os.makedirs(os.path.join(config_for_flask.DB_ROOT,"auxilary","blog"))
    # # config.DIR_DB_AUX_BLOG directory:
    # if not os.path.exists(os.path.join(config_for_flask.DB_ROOT,"auxilary","blog","posts")):
    #     os.makedirs(os.path.join(config_for_flask.DB_ROOT,"auxilary","blog","posts"))

    # config.DIR_DB_AUXILARY directory:
    if not os.path.exists(config_for_flask.DIR_DB_AUXILARY):
        os.makedirs(config_for_flask.DIR_DB_AUXILARY)
    # config.DIR_DB_AUX_IMAGES_PEOPLE directory:
    if not os.path.exists(config_for_flask.DIR_DB_AUX_IMAGES_PEOPLE):
        os.makedirs(config_for_flask.DIR_DB_AUX_IMAGES_PEOPLE)
    # config.DIR_DB_AUX_BLOG directory:
    if not os.path.exists(config_for_flask.DIR_DB_AUX_BLOG):
        os.makedirs(config_for_flask.DIR_DB_AUX_BLOG)
    # config.DIR_DB_AUX_BLOG_POSTS directory:
    if not os.path.exists(config_for_flask.DIR_DB_AUX_BLOG_POSTS):
        os.makedirs(config_for_flask.DIR_DB_AUX_BLOG_POSTS)


    ############################################################################
    ## Build Sqlite database files
    #Build DB_NAME_USERS
    
    if os.path.exists(os.path.join(config_for_flask.DB_ROOT,os.environ.get('DB_NAME_USERS'))):
        logger_init.info(f"db already exists: {os.path.join(config_for_flask.DB_ROOT,os.environ.get('DB_NAME_USERS'))}")
    else:
        dict_base['Base_users'].metadata.create_all(dict_engine['engine_users'])
        logger_init.info(f"NEW db created: {os.path.join(config_for_flask.DB_ROOT,os.environ.get('DB_NAME_USERS'))}")

    #Build DB_NAME_CAGE
    if os.path.exists(os.path.join(config_for_flask.DB_ROOT,os.environ.get('DB_NAME_CAGE'))):
        logger_init.info(f"db already exists: {os.path.join(config_for_flask.DB_ROOT,os.environ.get('DB_NAME_CAGE'))}")
    else:
        dict_base['Base_cage'].metadata.create_all(dict_engine['engine_cage'])
        logger_init.info(f"NEW db created: {os.path.join(config_for_flask.DB_ROOT,os.environ.get('DB_NAME_CAGE'))}")

    #Build DB_NAME_BLS
    if os.path.exists(os.path.join(config_for_flask.DB_ROOT,os.environ.get('DB_NAME_BLS'))):
        logger_init.info(f"db already exists: {os.path.join(config_for_flask.DB_ROOT,os.environ.get('DB_NAME_BLS'))}")
    else:
        dict_base['Base_bls'].metadata.create_all(dict_engine['engine_bls'])
        logger_init.info(f"NEW db created: {os.path.join(config_for_flask.DB_ROOT,os.environ.get('DB_NAME_BLS'))}")

    logger_init.info(f"- SQL_URI_USERS: sqlite:///{config_for_flask.DB_ROOT}{os.environ.get('DB_NAME_USERS')}")

    from app_package.bp_main.routes import bp_main
    from app_package.bp_users.routes import bp_users
    from app_package.bp_admin.routes import bp_admin
    from app_package.bp_error.routes import bp_error
    from app_package.bp_blog.routes import bp_blog

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_error)
    app.register_blueprint(bp_blog)

    return app