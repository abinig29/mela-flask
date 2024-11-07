from flask import render_template, redirect, url_for, flash, jsonify
from app.model.job import Category
from app.extension import db
from . import admin_category
from flask_login import login_required
from app.forms import CategoryForm


@admin_category.route("/", methods=["GET", "POST"])
@login_required
def list_categories():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data)
        db.session.add(new_category)
        db.session.commit()
        flash("Category added successfully!", "success")
        return redirect(url_for("admin_category.list_categories"))

    categories = Category.query.all()
    return render_template("category.html", form=form, categories=categories)
