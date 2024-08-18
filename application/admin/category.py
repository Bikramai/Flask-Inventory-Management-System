from flask import request, render_template, flash, url_for, redirect

from application.admin import admin, admin_required
from application.databaseModel import Category
from application.extension import db


@admin.route('/categories', methods=['GET', 'POST'])
@admin_required
def create_category():
    if request.method == 'POST':
        name = request.form.get('name').lower()
        description = request.form.get('description')
        existing_category = Category.query.filter(Category.name == name).first()
        if existing_category:
            flash("A category with the same name already exists.", "danger")
        else:
            category = Category(name=name, description=description)
            db.session.add(category)
            db.session.commit()
            flash("Category added successfully!", "success")
        return redirect(url_for("admin.create_category"))

    categories = Category.query.all()

    return render_template('categories.html', categories=categories)


@admin.route('/delete_category/<int:id>')
@admin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    if category is None:
        flash("Category not found", "danger")
    else:
        db.session.delete(category)
        db.session.commit()
        flash("Category deleted successfully!", "success")
    return redirect(url_for("admin.create_category"))


@admin.route('/update_category/<int:id>', methods=['POST'])
@admin_required
def update_category(id):
    category = Category.query.get(id)
    if category is None:
        flash("Category not found", "danger")
        return redirect(url_for("admin.create_category"))
    if request.method == 'POST':
        category.name = request.form.get('name').lower()
        category.description = request.form.get('description')
        db.session.commit()
        flash("Category updated successfully!", "success")
    return redirect(url_for("admin.create_category"))
