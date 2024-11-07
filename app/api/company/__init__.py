from flask import Blueprint
from flask_restful import Api
from .create_company import CreateCompany
from .get_company import GetCompany
from .edit_company import EditCompany
from .post_job import PostJob
from .get_jobs import GetCompanyJobs

company_bp = Blueprint("company", __name__)
api = Api(company_bp)
api.add_resource(CreateCompany, "/")
api.add_resource(GetCompany, "/")
api.add_resource(EditCompany, "/")
api.add_resource(PostJob, "/post-job")
api.add_resource(GetCompanyJobs, "/get-job")
