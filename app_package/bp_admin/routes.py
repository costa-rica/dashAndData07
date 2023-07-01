
from flask import Blueprint
from flask import render_template, url_for, redirect, flash, request, \
    abort, session, Response, current_app, send_from_directory, make_response
import bcrypt
from flask_login import login_required, login_user, logout_user, current_user
import logging
from logging.handlers import RotatingFileHandler
import os
import json


#Setting up Logger
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
formatter_terminal = logging.Formatter('%(asctime)s:%(filename)s:%(name)s:%(message)s')

#initialize a logger
logger_bp_admin = logging.getLogger(__name__)
logger_bp_admin.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler(os.path.join(os.environ.get('WEB_ROOT'),'logs','bp_admin.log'), mode='a', maxBytes=5*1024*1024,backupCount=2)
file_handler.setFormatter(formatter)

#where the stream_handler will print
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter_terminal)

# logger_sched.handlers.clear() #<--- This was useful somewhere for duplicate logs
logger_bp_admin.addHandler(file_handler)
logger_bp_admin.addHandler(stream_handler)

bp_admin = Blueprint('bp_admin', __name__)


@bp_admin.before_request
def before_request():
    logger_bp_admin.info(f"-- ***** in before_request route --")
    ###### TEMPORARILY_DOWN: redirects to under construction page ########
    if os.environ.get('TEMPORARILY_DOWN') == '1':
        if request.url != request.url_root + url_for('bp_main.temporarily_down')[1:]:
            # logger_bp_users.info("*** (logger_bp_users) Redirected ")
            logger_bp_admin.info(f'- request.referrer: {request.referrer}')
            logger_bp_admin.info(f'- request.url: {request.url}')
            return redirect(url_for('bp_main.temporarily_down'))



@bp_admin.route('/admin_page', methods = ['GET', 'POST'])
@login_required
def admin_page():
    logger_admin.info('- in admin_db -')
    logger_admin.info(f"current_user.admin: {current_user.admin}")

    if not current_user.admin:
        return redirect(url_for('main.rincons'))
    
    rincon_users = sess.query(Users).all()

    col_names = ["username"]

    if request.method == "POST":
        formDict = request.form.to_dict()
        # print("formDict: ", formDict)
        if formDict.get("update_user_privileges"):
            del formDict['update_user_privileges']
            update_list = []
            for user_rincon, permission_bool_str in formDict.items():
                underscore_user, underscore_rincon = user_rincon.split(",")
                _,user_id = underscore_user.split("_")
                _,rincon_id = underscore_rincon.split("_")
                user_rincon_assoc = sess.query(UsersToRincons).filter_by(users_table_id=user_id, rincons_table_id=rincon_id).first()
                permission_bool = False if permission_bool_str == "false" else True
                if user_rincon_assoc.permission_admin != permission_bool:
                    # print("* user_rincon_assoc.permission_admin != permission_bool *")
                    # print("user_rincon_assoc: ", user_rincon_assoc)
                    # print("user_rincon_assoc, ricon_admin_permission: ", type(user_rincon_assoc.permission_admin), user_rincon_assoc.permission_admin)
                    # print("formDict permission_bool_str: ", type(permission_bool_str), permission_bool_str)
                    user_rincon_assoc.permission_admin = permission_bool
                    sess.commit()

                    user_updated = sess.get(Users, user_id)
                    rincon_updated = sess.get(Rincons, rincon_id)

                    if permission_bool:
                        update_list.append(f"Successfully updated {user_updated.username} to admin ({permission_bool}) for  {rincon_updated.name}")
                    else:
                        update_list.append(f"{user_updated.username} is no longer an admin ({permission_bool}) for  {rincon_updated.name}")


                    


                    # if permission_bool:
                    #     flash(f"Successfully updated {user_updated.username} to admin ({permission_bool}) for  {rincon_updated.name}", "success")
                    #     return redirect(request.url)
                    
                    # flash(f"{user_updated.username} is no longer an admin ({permission_bool}) for  {rincon_updated.name}", "warning")
            if len(update_list) > 0 :
                for count, i in enumerate(update_list):
                    if count == 0:
                        flash_update_string = i
                    else:
                        flash_update_string = f"{flash_update_string},\n{i}"
                flash(flash_update_string, "success")
            return redirect(request.url)



    return render_template('admin/admin.html', rincon_users=rincon_users, col_names=col_names)
