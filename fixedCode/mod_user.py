import sqlite3

import flask
from flask import Blueprint, render_template, redirect, request, g, session, make_response, flash
import libuser
import libsession
import libmfa
import audit

mod_user = Blueprint('mod_user', __name__, template_folder='templates')


@mod_user.route('/login', methods=['GET', 'POST'])
def do_login():

    session.pop('username', None)

    if request.method == 'POST':

        username_input = request.form.get('username')
        password = request.form.get('password')
        otp = request.form.get('otp')
        if libuser.is_locked(username_input):
            audit.logEvent("Login_Locked", username_input, request.remote_addr, "Account is locked due to too many failed attempts")
            flash("Account is locked due to too many attempts. Try again later.")
            return render_template('user.login.mfa.html')

        username = libuser.login(username_input, password)

        if not username:
            audit.logEvent("Login_Failed", username_input, request.remote_addr, "Invalid username or password")
            libuser.increment_failed_attempts(username_input)

            if libuser.get_failed_attempts(username_input) >= libuser.MAX_FAILED_ATTEMPTS:
                flask.flash("Exceeded Password attempts. Try again later.")
                libuser.lock_account(username_input)
            else:
                flash("Invalid Username or Password")
            return render_template('user.login.mfa.html')


        libuser.set_failed_attempts(username_input, 0)
        libuser.unlock_account(username_input)

        if libmfa.mfa_is_enabled(username):
            if not libmfa.mfa_validate(username, otp):
                audit.logEvent("Login_MFA_Failed", username, request.remote_addr, "Invalid OTP")
                flash("Invalid OTP")
                return render_template('user.login.mfa.html')
            
        audit.logEvent("Login_Success", username, request.remote_addr, "Successful authentication")

        response = make_response(redirect('/'))
        response = libsession.create(request=request, response=response, username=username)
        return response

    return render_template('user.login.mfa.html')


@mod_user.route('/create', methods=['GET', 'POST'])
def do_create():

    session.pop('username', None)

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('password')
        libuser.user_create(username, password)
        session['username'] = libuser.login(username, password)

        if session['username']:
            return redirect('/')

    return render_template('user.create.html')


@mod_user.route('/chpasswd', methods=['GET'])
def do_chpasswd_get():
    return render_template('user.chpasswd.html')


@mod_user.route('/chpasswd', methods=['POST'])
def do_chpasswd_post():

    if 'username' not in g.session:
        return redirect('/')

    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    new_password_again = request.form.get('new_password_again')

    if not libuser.login(g.session['username'], current_password):
        flash("Invalid current password")
        return render_template('user.chpasswd.html')

    if new_password != new_password_again:
        flash("The passwords don't match")
        return render_template('user.chpasswd.html')

    if not libuser.is_password_allowed(new_password):
        flash("The password don't comply our requirements, please, choose another one.")
        return render_template('user.chpasswd.html')

    libuser.password_set(g.session['username'], new_password)
    audit.logEvent("Password_Change", g.session['username'], request.remote_addr, "Password changed successfully")
    
    flash("Password changed")
    return redirect('/')

@mod_user.route('/logout', methods=['GET'])
def do_logout():

    if 'username' in g.session:
        audit.logEvent("Logout", g.session['username'], request.remote_addr, "User logged out")

    session.pop('username', None)
    
    response = make_response(redirect('/user/login'))
    response = libsession.destroy(response)

    flash("Logged out successfully")
    return response

@mod_user.route('/logs', methods=['GET'])
def view_logs():
    
    if 'username' not in g.session:
        flash("You must be logged in to view logs")
        return redirect('/user/login')
    if g.session['username'] != 'admin':
        flash("You do not have permission to view logs")
        return redirect('/')

    try:
        with open('logs/audit.log', 'r') as f:
            logs = f.readlines()
        logs = logs[-100:]
        logs.reverse()
        logs = ''.join(logs)
    except FileNotFoundError:
        logs = ["No logs found."]

    return render_template('logs.html', logs=logs)