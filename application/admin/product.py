import os

from flask import render_template, request, redirect, url_for, flash

import time

from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from application.admin import admin, admin_required
from application.databaseModel import Category, Product, Notifications
from application.extension import db


@admin.route("/add_product", methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        product_name = request.form.get('product-name')
        category_id = int(request.form.get('product-category'))
        product_description = request.form.get('product-desc')
        product_price = float(request.form.get('product-price'))
        product_link = request.form.get('product-link')

        # Handle the image file
        image = request.files['product-image']
        filename = secure_filename(image.filename)
        # Append a timestamp to the filename to make it unique
        filename = f"{int(time.time())}_{filename}"
        # Ensure the directory exists
        os.makedirs(os.path.join("application", "static", "product_image"), exist_ok=True)

        image.save(os.path.join("application", "static", "product_image", filename))

        new_product = Product(
            name=product_name,
            category_id=category_id,
            description=product_description,
            price=product_price,
            purchase_link=product_link,
            image_path=filename  # Add the image path to the product
        )

        db.session.flush()

        notification = Notifications()
        notification.product_addition_notification(new_product)

        db.session.add(new_product)
        db.session.add(notification)
        db.session.commit()

        flash("Product Added Successfully!", "success")

        return redirect(url_for('admin.add_product'))

    categories = Category.query.all()
    return render_template("add_product.html", categories=categories)


@admin.route("/view_all_product", methods=['GET'])
@admin_required
def view_all_product():
    products = Product.query.order_by(Product.id.desc())
    page_heading = "All Products"
    return render_template("view_all_products.html"
                           , products=products
                           , page_heading=page_heading)


@admin.route("/view_product/<int:product_id>", methods=['GET'])
@admin_required
def view_product(product_id):
    product = Product.query.get_or_404(product_id)

    return render_template("view_product.html"
                           , product=product)


@admin.route("/delete_product/<int:product_id>", methods=['GET', 'POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash(f"Product {product.name[:10]} Deleted successfully", "info")

    return redirect(url_for("admin.view_all_product"))

# TODO: ADD FEATURE TO EDIT PRODUCT
