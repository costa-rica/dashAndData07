from flask import Blueprint
from flask import render_template, url_for, redirect, flash, request, \
    abort, session, Response, current_app, send_from_directory, make_response
import os
import logging
from logging.handlers import RotatingFileHandler


bp_main = Blueprint('bp_main', __name__)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
formatter_terminal = logging.Formatter('%(asctime)s:%(filename)s:%(name)s:%(message)s')

logger_bp_main = logging.getLogger(__name__)
logger_bp_main.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler(os.path.join(os.environ.get('WEB_ROOT'),'logs','bp_main_routes.log'), mode='a', maxBytes=5*1024*1024,backupCount=2)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter_terminal)

logger_bp_main.addHandler(file_handler)
logger_bp_main.addHandler(stream_handler)


@bp_main.before_request
def before_request():
    logger_bp_main.info(f"-- ***** in before_request route --")
    ###### TEMPORARILY_DOWN: redirects to under construction page ########
    if os.environ.get('TEMPORARILY_DOWN') == '1':
        if request.url != request.url_root + url_for('bp_main.temporarily_down')[1:]:
            # logger_bp_users.info("*** (logger_bp_users) Redirected ")
            logger_bp_main.info(f'- request.referrer: {request.referrer}')
            logger_bp_main.info(f'- request.url: {request.url}')
            return redirect(url_for('bp_main.temporarily_down'))

@bp_main.route("/", methods=["GET","POST"])
def home():
    logger_bp_main.info(f"-- in home page route --")

    return render_template('main/home.html')


# Custom static data
@bp_main.route('/<dir_name>/<filename>')
def file_DB_ROOT(dir_name, filename):
    # print("-- enterd custom static -")
    # name_no_spaces = ""
    # dir_name = 
    
    return send_from_directory(os.path.join(current_app.config.get('DB_ROOT'),"files", dir_name), filename)




# Custom static data - DIR_DB_AUXILARY (/_databases/dashAndData07/auxilary/<aux_dir_name>/<filename>)
@bp_main.route('/get_aux_file_from_dir/<aux_dir_name>/<filename>')
def get_aux_file_from_dir(aux_dir_name, filename):
    logger_bp_main.info(f"- in get_aux_file_from_dir route")
    
    return send_from_directory(os.path.join(current_app.config.get('DB_ROOT'),"auxilary", aux_dir_name), filename)



