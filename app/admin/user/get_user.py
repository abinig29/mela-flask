from flask import jsonify, request, render_template
from . import admin_user
from app import db  # Import your database instance
from app.model import User, RoleType  # Assuming User model is in models.py
from app.config.const import per_page


def search_users(query, page, per_page):
    # Filter users based on the USER role and the search query
    filtered_users = (
        User.query.join(User.profile)
        .filter(
            (User.role == RoleType.USER.name)  # Ensure the user role is USER
            & (
                # (User.profile.first_name.ilike(f"%{query}%"))
                # | (User.profile.last_name.ilike(f"%{query}%"))
                # | (User.email.ilike(f"%{query}%"))
                (User.email.ilike(f"%{query}%"))
            )
        )
        .all()
    )

    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = filtered_users[start:end]

    user_data = [
        {
            "id": str(user.id),
            "full_name": f"{user.profile.first_name} {user.profile.last_name}",
            "email": user.email,
            "phone_number": user.profile.phone_number,
            "active_status": user.active,
        }
        for user in paginated_users
    ]

    return user_data, len(filtered_users)


@admin_user.route("/")
def user():
    return render_template("user.html")


@admin_user.route("/paginate")
def paginate_user():
    page = int(request.args.get("page", 1))
    search_query = request.args.get("search", "").strip()

    user_data = []  # Initialize user_data here

    if search_query:
        paginated_users, total_count = search_users(search_query, page, per_page)
        user_data = paginated_users  # Use the result from search_users
    else:
        # Count and get users with USER role without search query
        total_count = User.query.filter_by(
            role=RoleType.USER.name
        ).count()  # Use the RoleType enum
        paginated_users = (
            User.query.filter_by(
                role=RoleType.USER.name
            )  # Ensure we're filtering by USER role
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        user_data = [
            {
                "id": str(user.id),
                "full_name": (
                    f"{user.profile.first_name} {user.profile.last_name}"
                    if user.profile
                    else "N/A"
                ),
                "email": user.email,
                "phone_number": user.profile.phone_number if user.profile else "N/A",
                "active_status": user.active,
            }
            for user in paginated_users
        ]

    total_pages = (total_count + per_page - 1) // per_page
    return jsonify({"users": user_data, "totalPages": total_pages, "currentPage": page})
