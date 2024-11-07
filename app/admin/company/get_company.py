from flask import jsonify, request, render_template
from . import admin_company  # Ensure you have a blueprint for company management
from app.config.const import per_page  # Assuming per_page is defined here
from app.model import Company


def search_companies(query, page, per_page):
    # Filtering companies based on search query
    filtered_companies = (
        Company.query.filter(
            (Company.name.ilike(f"%{query}%")) | (Company.email.ilike(f"%{query}%"))
        )
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    total_count = Company.query.filter(
        (Company.name.ilike(f"%{query}%")) | (Company.email.ilike(f"%{query}%"))
    ).count()

    return filtered_companies, total_count


@admin_company.route("/")
def company():
    return render_template("company.html")


@admin_company.route("/paginate_company")
def paginate_company():
    page = int(request.args.get("page", 1))
    search_query = request.args.get("search", "").strip()

    if search_query:
        paginated_companies, total_count = search_companies(
            search_query, page, per_page
        )
    else:
        paginated_companies = (
            Company.query.offset((page - 1) * per_page).limit(per_page).all()
        )
        total_count = Company.query.count()  # Count total companies

    total_pages = (total_count + per_page - 1) // per_page
    return jsonify(
        {
            "companies": [company.to_dict() for company in paginated_companies],
            "totalPages": total_pages,
            "currentPage": page,
        }
    )
