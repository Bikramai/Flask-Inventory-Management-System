import os

from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user

from application.admin import admin, admin_required
from application.databaseModel import User, Contacts
from application.extension import db, bcrypt


@admin.route("/view_users")
@admin_required
def view_users():
    non_admin_users = User.query.filter(User.id != current_user.id).all()
    return render_template("view_users.html", users=non_admin_users)


@admin.route("/edit_user/<int:user_id>", methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = 'is_admin' in request.form

        if username:
            user.username = username
        if password:
            user.password = bcrypt.generate_password_hash(password)
        if is_admin:
            user.is_admin = is_admin

        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('admin.view_users'))

    return render_template("edit_user.html", user=user)


@admin.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.username} deleted successfully", "danger")
    return redirect(url_for('admin.view_users'))


@admin.route("/suspend_user/<int:user_id>")
def suspend_user(user_id):
    user = User.query.get_or_404(user_id)

    user.is_suspended = True
    db.session.commit()

    flash(f"User {user.username} suspended successfully", "warning")
    return redirect(url_for('admin.view_users'))


@admin.route("/unsuspend_user/<int:user_id>")
def unsuspend_user(user_id):
    user = User.query.get_or_404(user_id)

    user.is_suspended = False
    db.session.commit()

    flash(f"User {user.username} unsuspended successfully", "warning")
    return redirect(url_for('admin.view_users'))


@admin.route("/view_activities/<int:user_id>")
def view_activities(user_id):
    user = User.query.get_or_404(user_id)
    log_folder = os.path.join(current_app.root_path, 'static', 'logs')
    log_file = os.path.join(log_folder, f'{user.username}.log')

    # Read the log file
    with open(log_file, 'r') as f:
        log_content = f.readlines()

    # Reverse the log content
    log_content = log_content[::-1]

    return render_template("view_activities.html", username=user.username, log_content=log_content)


@admin.route("/view_query")
def view_query():

    query = Contacts.query.order_by(Contacts.id.desc())

    return render_template("query.html"
                           , query=query)
