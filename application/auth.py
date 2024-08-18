from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user

from application.extension import bcrypt, db, log_message
from .databaseModel import User

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.view_all_product"))
        else:
            return redirect(url_for("user.view_products"))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username exists
        user = User.query.filter_by(username=username).first()
        if user:

            if user.is_suspended:
                flash("Your account has been suspended! Please contact admin!", "danger")
                return redirect(url_for("auth.login"))

            # Verify password
            if bcrypt.check_password_hash(user.password_hash, password):
                login_user(user)
                log_message(current_user.username, "Log In")
                if user.is_admin:
                    return redirect(url_for('admin.view_all_product'))
                else:
                    return redirect(url_for('user.view_products'))
            else:
                flash('Invalid password', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Username does not exist', 'danger')
            return redirect(url_for('auth.login'))

    return render_template("login.html")


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.view_all_product"))
        else:
            return redirect(url_for("user.view_products"))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords must match', 'danger')
            return redirect(url_for('auth.register'))

        # Check if username exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password)

        # Create new user
        new_user = User()
        new_user.username = username
        new_user.password_hash = hashed_password
        new_user.profile_picture = "default.jpg"
        new_user.is_admin = False

        log_message(username, "New Account Created")

        # Save user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully', 'success')
        return redirect(url_for('auth.login'))

    return render_template("register.html")


@auth.route("/logout")
def logout():

    if current_user.is_authenticated:
        log_message(current_user.username, "Logged Out")
        logout_user()
        flash('Logged out successfully', 'info')
    return redirect(url_for('auth.login'))
