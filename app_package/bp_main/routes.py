from flask import Blueprint
from flask import render_template, url_for, redirect, flash, request, \
    abort, session, Response, current_app, send_from_directory, make_response
import os
import logging
from logging.handlers import RotatingFileHandler
from app_package import secure_headers
import requests
from app_package.bp_main.utils import send_confirm_email, send_message_to_nick

bp_main = Blueprint('bp_main', __name__)
# sess_users = dict_sess['sess_users']

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



#This is to get the security headers on home page
@bp_main.after_request
def set_secure_headers(response):
    secure_headers.framework.flask(response)
    logger_bp_main.info("- in @bp_main.after_request")
    return response

@bp_main.before_request
def before_request():
    logger_bp_main.info(f"- in bp_main.before_request route --")
    ###### TEMPORARILY_DOWN: redirects to under construction page ########
    if os.environ.get('TEMPORARILY_DOWN') == '1':
        if request.url != request.url_root + url_for('bp_main.temporarily_down')[1:]:
            logger_bp_main.info(f'- request.referrer: {request.referrer}')
            logger_bp_main.info(f'- request.url: {request.url}')
            return redirect(url_for('bp_main.temporarily_down'))

@bp_main.route("/", methods=["GET","POST"])
def home():
    logger_bp_main.info(f"-- in home page route --")
    on_home_page = True

    return render_template('main/home.html', site_key=current_app.config.get('SITE_KEY_CAPTCHA'),
        on_home_page = on_home_page)


# Custom static data
@bp_main.route('/<dir_name>/<filename>')
def file_DB_ROOT(dir_name, filename):   
    return send_from_directory(os.path.join(current_app.config.get('DB_ROOT'),"files", dir_name), filename)




# Custom static data - DIR_DB_AUXILARY (/_databases/dashAndData07/auxilary/<aux_dir_name>/<filename>)
@bp_main.route('/get_aux_file_from_dir/<aux_dir_name>/<filename>')
def get_aux_file_from_dir(aux_dir_name, filename):
    logger_bp_main.info(f"- in get_aux_file_from_dir route")
    return send_from_directory(os.path.join(current_app.config.get('DB_ROOT'),"auxilary", aux_dir_name), filename)



########################
# recaptcha
########################

# @bp_main.route("/sign-user-up", methods=['POST'])
@bp_main.route("/send_me_a_message", methods=['POST'])
# def sign_up_user():
def send_me_a_message():
    # print(request.form)
    secret_response = request.form['g-recaptcha-response']

    verify_response = requests.post(url=f"{current_app.config.get('VERIFY_URL_CAPTCHA')}?secret={current_app.config.get('SECRET_KEY_CAPTCHA')}&response={secret_response}").json()
    print(verify_response)
    if verify_response['success'] == False or verify_response['score'] < 0.5:
        abort(401)

    formDict = request.form.to_dict()
    print(formDict)
    
    # get email, name and message
    senders_name = formDict.get('name')
    senders_email = formDict.get('email')
    senders_message = formDict.get('message')

    # send message to nick@dashanddata.com
    try:
        send_message_to_nick(senders_name, senders_email, senders_message)
        logger_bp_main.info('- send_message_to_nick succeeded!')
    except:
        logger_bp_main.info('*** not successsuflly send_message_to_nick ***')
    # Send confirmation email to sender
    try:
        send_confirm_email(senders_name, senders_email, senders_message)
        logger_bp_main.info('- send_confirm_email succeeded!')
    except:
        logger_bp_main.info('*** not successsuflly send_confirm_email')
        flash(f'Problem with email: {senders_email}', 'warning')
        # return redirect(url_for('bp_users.login'))
        return redirect(url_for('bp_main.home'))

    flash(f'Message has been sent to nick@dashanddata.com. A verification has been sent to your email as well.', 'success')
    return redirect(url_for('bp_main.home'))
