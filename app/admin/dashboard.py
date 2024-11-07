from flask import Blueprint, render_template, Flask, request, jsonify
from datetime import datetime, timedelta
from random import randint
from app.extension import db
from flask_login import login_required
from sqlalchemy import func
from app.model import Company, Category, User, Job


dashboard_bp = Blueprint("admin_dashboard", __name__)


def generate_mock_data(hours):
    return [randint(5, 50) for _ in range(hours)]


@dashboard_bp.route("/")
@login_required
def dashboard():
    company_count = db.session.query(Company).count()
    user_count = db.session.query(User).count()
    job_count = db.session.query(Job).count()
    category_count = db.session.query(Category).count()

    return render_template(
        "dashboard.html",
        user_count=user_count,
        company_count=company_count,
        job_count=job_count,
        category_count=category_count,
    )


@dashboard_bp.route("/jobs")
@login_required
def get_jobs_scraped():
    time_frame = request.args.get("timeFrame")
    now = datetime.now()
    values_query = []

    if time_frame == "today":
        # Get the start and end of the current day
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1) - timedelta(microseconds=1)

        # Generate hourly labels for the current day
        labels = [
            f"{(start_of_day + timedelta(hours=i)).strftime('%H:%M')}"
            for i in range(24)
        ]
        print(start_of_day, end_of_day)

        # Query to count jobs posted per hour for today
        values_query = (
            db.session.query(
                func.to_char(Job.posted_date, "HH24").label("hour"),
                func.count(Job.id),
            )
            .filter(Job.posted_date >= start_of_day, Job.posted_date <= end_of_day)
            .group_by("hour")
            .order_by("hour")
            .all()
        )
        print(values_query)

    elif time_frame == "yesterday":
        start_of_yesterday = now - timedelta(days=1)
        start_of_yesterday = start_of_yesterday.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_of_yesterday = (
            start_of_yesterday + timedelta(days=1) - timedelta(microseconds=1)
        )

        labels = [
            f"{(start_of_yesterday + timedelta(hours=i)).strftime('%H:%M')}"
            for i in range(24)
        ]

        values_query = (
            db.session.query(
                func.to_char(Job.posted_date, "HH24").label("hour"),
                func.count(Job.id),
            )
            .filter(
                Job.posted_date >= start_of_yesterday,
                Job.posted_date <= end_of_yesterday,
            )
            .group_by("hour")
            .order_by("hour")
            .all()
        )

    elif time_frame == "last7days":
        seven_days_ago = now - timedelta(days=7)

        labels = [
            (now - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)
        ]

        values_query = (
            db.session.query(
                func.to_char(Job.posted_date, "YYYY-MM-DD").label("day"),
                func.count(Job.id),
            )
            .filter(Job.posted_date >= seven_days_ago)
            .group_by("day")
            .order_by("day")
            .all()
        )
        print("values_query", values_query)

    else:
        return jsonify({"error": "Invalid time frame"}), 400

    # Extract labels and counts for response
    values_dict = {label: 0 for label in labels}  # initialize all labels with 0 count
    for label, count in values_query:
        if time_frame in ["today", "yesterday"]:
            label = (
                f"{label}:00"  # Add minutes for hourly labels (e.g., "14" -> "14:00")
            )
        values_dict[label] = count

    values = [values_dict[label] for label in labels]

    return jsonify({"labels": labels, "values": values})


@dashboard_bp.route("/job-sources")
@login_required
def get_job_sources():
    results = (
        db.session.query(
            Job.source.label("source_name"), func.count(Job.id).label("job_count")
        )
        .group_by(Job.source)  # Group by job source
        .all()
    )

    source_names = [result.source_name for result in results]
    job_counts = [result.job_count for result in results]

    return jsonify({"source_names": source_names, "job_counts": job_counts})
