from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user

from application.databaseModel import Product, Review, Comment, Notifications
from application.extension import log_message, db
from application.user import user, user_required


@user.route("/")
@user_required
def view_products():
    log_message(current_user.username, "Visited All Product Page")
    products = Product.query.all()
    return render_template(
        "user/all_product.html", products=products, page_heading="All Products"
    )


@user.route("/favorites")
@user_required
def view_favorites():
    log_message(current_user.username, "Visited Favorites Page")
    favorite_products = current_user.favorite_products
    saved_reviews = current_user.bookmarked_reviews
    return render_template(
        "user/all_product.html",
        products=favorite_products,
        reviews=saved_reviews,
        page_heading="Favorite Products",
    )


@user.route("/add_to_favorites/<int:product_id>")
@user_required
def add_to_favorites(product_id):
    product = Product.query.get_or_404(product_id)
    log_message(current_user.username, f"Added <PRODUCT {product.id}> to Favourites")
    current_user.favorite_products.append(product)
    db.session.commit()
    return redirect(url_for("user.view_products"))


@user.route("/remove_from_favorites/<int:product_id>")
@user_required
def remove_from_favorites(product_id):
    product = Product.query.get_or_404(product_id)
    log_message(
        current_user.username, f"Removed <PRODUCT {product.id}> from Favourites"
    )
    current_user.favorite_products.remove(product)
    db.session.commit()
    return redirect(url_for("user.view_products"))


@user.route("/product/<int:product_id>")
@user_required
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    review_exists = Review.query.filter_by(
        user_id=current_user.id, product_id=product_id
    ).first()
    other_reviews = Review.query.filter_by(product_id=product_id, status=True).all()
    return render_template(
        "user/view_product.html",
        product=product,
        review_exists=review_exists,
        other_reviews=other_reviews,
    )


@user.route("/add_review/<int:product_id>", methods=["POST"])
@user_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    rating = request.form.get("rating")
    pros = request.form.get("pros")
    cons = request.form.get("cons")
    feedback = request.form.get("feedback")

    new_review = Review(
        rating=rating,
        pros=pros,
        cons=cons,
        content=feedback,
        user_id=current_user.id,
        product_id=product.id,
    )

    db.session.add(new_review)
    db.session.commit()

    flash("Your Review is submitted for approval", "success")

    return redirect(url_for("user.view_product", product_id=product_id))


@user.route("/add_to_bookmarks/<int:review_id>")
@user_required
def add_to_bookmarks(review_id):
    review = Review.query.get_or_404(review_id)
    log_message(current_user.username, f"Added <REVIEW {review.id}> to Bookmarks")
    current_user.bookmarked_reviews.append(review)
    db.session.commit()
    return redirect(url_for("user.view_product", product_id=review.product_id))


@user.route("/remove_from_bookmarks/<int:review_id>")
@user_required
def remove_from_bookmarks(review_id):
    review = Review.query.get_or_404(review_id)
    log_message(current_user.username, f"Removed <REVIEW {review.id}> from Bookmarks")
    current_user.bookmarked_reviews.remove(review)
    db.session.commit()
    return redirect(url_for("user.view_product", product_id=review.product_id))


@user.route("/add_comment/<int:review_id>", methods=["POST"])
@user_required
def add_comment(review_id):
    review = Review.query.get_or_404(review_id)
    comment_content = request.form.get("content")
    new_comment = Comment(
        content=comment_content, user_id=current_user.id, review_id=review.id
    )

    notification = Notifications()
    notification.review_comment_notification(review=review)

    if notification:
        db.session.add(notification)

    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for("user.view_product", product_id=review.product_id))
