from flask import Blueprint, request, render_template, redirect
from flask_login import login_required, current_user

from application.databaseModel import Review, Product, Category, User

search = Blueprint("search", __name__, url_prefix="/search")


@search.route("/")
def search_query():
    query = request.args.get("q", None, type=str)

    if not query:
        return redirect("/")
    products = Product.query.filter(Product.name.like(f'%{query}%')).all()

    if not current_user.is_authenticated:
        return render_template("search.html"
                           , reviews=None
                           , products=products
                           , categories=None
                           , users=None)

    reviews = Review.query.filter(Review.content.like(f'%{query}%'))

    if current_user.is_admin:
        categories = Category.query.filter(Category.name.like(f'%{query}%')).all()
        users = User.query.filter(User.username.like(f'%{query}%')).all()
        reviews = reviews.all()
    else:
        categories = None
        users = None
        reviews = reviews.filter(Review.status == True).all()

    return render_template("search.html"
                           , reviews=reviews
                           , products=products
                           , categories=categories
                           , users=users)
