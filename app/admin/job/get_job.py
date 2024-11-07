from flask import Flask, jsonify, request, render_template
from app.config.const import per_page
from . import admin_job
from flask_login import login_required
from app.model import Job  # Import the Job model


@admin_job.route("/")
@login_required
def job():
    return render_template("job.html")


@admin_job.route("/paginate", methods=["GET"])
@login_required
def paginate_job():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str)
    source = request.args.get("source", "", type=str)

    query = Job.query

    if search:
        query = query.filter(Job.title.ilike(f"%{search}%"))  # Filter by title

    if source:
        query = query.filter(Job.source.ilike(f"%{source}%"))  # Filter by source

    total_count = query.count()
    jobs = query.offset((page - 1) * per_page).limit(per_page).all()
    total_pages = (total_count + per_page - 1) // per_page

    return jsonify(
        {
            "jobs": [job.to_dict() for job in jobs],  # Assuming a to_dict method exists
            "totalPages": total_pages,
            "currentPage": page,
        }
    )
