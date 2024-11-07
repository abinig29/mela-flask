from flask import Blueprint
from flask_restful import Api
from .register import Register
from .login import Login
from .forgot_password import ForgotPassword
from .verify_otp import VerifyOTP
from .reset_password import ResetPassword
from .change_password import ChangePassword


auth_bp = Blueprint("auth", __name__)
api = Api(auth_bp)
api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(ForgotPassword, "/forgot-password")
api.add_resource(VerifyOTP, "/verify-otp")
api.add_resource(ResetPassword, "/reset-password")
api.add_resource(ChangePassword, "/change-password")
