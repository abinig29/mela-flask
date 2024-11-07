from flask import jsonify, request, flash, render_template, redirect
from . import admin_company


companies = [
    {
        "id": i,
        "name": f"Company {i} Name",
        "email": f"company{i}@example.com",
        "website": f"www.company{i}.com",
        "jobs_count": i * 2,
    }
    for i in range(1, 101)
]


@admin_company.route("/<int:user_id>", methods=["GET", "DELETE"])
def single_user(user_id):
    global users
    if request.method == "GET":
        user = next((user for user in users if user["id"] == user_id), None)
        if user:
            return render_template("user_detail.html", user=user)
        else:
            flash("User not found", category="danger")
            return redirect("url_for('admin_user.user')")

    if request.method == "DELETE":
        users = [user for user in users if user["id"] != user_id]
        flash("user deleted successfully", category="success")
        return jsonify({"message": "User deleted successfully"}), 204
