from flask import flash, redirect, url_for, request
from . import admin_category
from app import db
from app.model.job import Category
from flask_login import login_required
from uuid import UUID


@admin_category.route("/<uuid:category_id>", methods=["POST"])
@login_required
def delete_category(category_id):
    category = Category.query.get(category_id)

    if not category:
        flash("Category not found", "error")
        return redirect(url_for("admin_category.list_categories"))

    db.session.delete(category)
    db.session.commit()

    flash("Category deleted successfully", "success")
    return redirect(url_for("admin_category.list_categories"))
