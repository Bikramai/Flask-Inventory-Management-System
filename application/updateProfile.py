from flask import request, Blueprint, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from application.extension import db, bcrypt
import os

profile = Blueprint("profile", __name__, url_prefix="/profile")


@profile.route("/update_profile", methods=["GET", "POST"])
@login_required
def update_profile():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        profile_pic = request.files["profile_pic"]
        # Ensure the directory exists
        os.makedirs(os.path.join("application", "static", "images"), exist_ok=True)
        # Save the profile picture in the 'application/static/profile' directory

        if profile_pic:
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join("application", "static", "images", filename))
            current_user.profile_picture = filename

        current_user.username = username
        if password:
            current_user.password_hash = bcrypt.generate_password_hash(password)

        db.session.commit()
        flash("Profile Updated Successfully!", "success")
        return redirect(url_for("profile.update_profile"))
    return render_template("update_profile.html")
