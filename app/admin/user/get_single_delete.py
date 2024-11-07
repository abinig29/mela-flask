from flask import jsonify, request, flash, render_template, redirect
from . import admin_user
from uuid import UUID
from app.model.user import User


@admin_user.route("/<uuid:user_id>", methods=["GET", "DELETE"])
def single_user(user_id):
    global users
    if request.method == "GET":
        user = User.query.get(user_id)
        if user:
            return render_template("user_detail.html", user=user)
        else:
            flash("User not found", category="danger")
            return redirect("url_for('admin_user.user')")

    if request.method == "DELETE":
        # users = [user for user in users if user["id"] != user_id]
        flash("user deleted successfully", category="success")
        return jsonify({"message": "User deleted successfully"}), 204
