from flask import Blueprint, render_template, request, flash, url_for, redirect
from sqlalchemy import func, desc

from application import db
from application.databaseModel import Product, Category, Contacts

route = Blueprint("route", __name__)


@route.route("/")
def index():
    header_product = Product.query.order_by(func.random()).first()
    categories = Category.query.all()
    products_by_category = []
    for category in categories:
        products = Product.query.filter_by(category_id=category.id).order_by(desc(Product.id)).limit(4).all()
        products_by_category.append((category, products))

    return render_template("home.html"
                           , header_product=header_product
                           , products_by_category=products_by_category)


@route.route("/about")
def about():
    return render_template("about.html")


@route.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        message = request.form.get('message')

        new_query = Contacts(fullname=fullname, email=email, message=message)
        db.session.add(new_query)
        db.session.commit()

        flash("Thankyou for contacting us!", "success")
        return redirect(url_for("route.contact"))
    
    return render_template("contact.html")
