from flask import redirect, render_template, request, url_for
from application.admin import admin, admin_required
from application.databaseModel import Review
from application.extension import db


@admin.route("/view_reviews")
@admin_required
def view_reviews():
    review_status = request.args.get("status", "New", type=str)

    if review_status == "New":
        reviews = Review.query.filter_by(status=False)
    elif review_status == "Approved":
        reviews = Review.query.filter_by(status=True)
    else:
        reviews = Review.query

    reviews = reviews.all()

    status = ["New", "Approved", "All"]

    return render_template(
        "view_reviews.html",
        reviews=reviews,
        status=status,
        default_status=review_status,
    )


@admin.route("/approve_review/<int:review_id>")
@admin_required
def approve_review(review_id):
    review = Review.query.get_or_404(review_id)
    review.status = True
    db.session.commit()
    return redirect(url_for("admin.view_reviews"))


@admin.route("/delete_review/<int:review_id>")
@admin_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for("admin.view_reviews"))
