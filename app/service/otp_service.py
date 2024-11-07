import time
from app.extension import db
from app.model import User


def check_otp(email, otp):
    """
    Verify the OTP for a given user email.

    Args:
        email (str): User's email.
        otp (str): The OTP code provided by the user.

    Returns:
        bool: True if OTP is valid, False if not.
        dict: A dictionary containing an error message if OTP verification fails.
    """
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False, {"error": "Email not found."}, 404
    if user.verification_code_expires is None:
        return False, {"error": "OTP verification has not been initiated."}, 400
    if user.verification_code_expires < int(time.time()):
        return False, {"error": "OTP has expired."}, 400

    if not user.check_verification_code(otp):
        return False, {"error": "Invalid OTP."}, 400

    user.verification_code_hash = None
    user.verification_code_expires = None
    db.session.commit()

    return True, {"message": "OTP verified successfully."},200


def reset_password(email, otp, new_password):

    user = User.query.filter_by(email=email).first()
    if user is None:
        return {"error": "Email not found."}, 404
    otp_verified, response, status_code = check_otp(email, otp)
    if not otp_verified:
        return response, status_code
    user.set_password(new_password)
    db.session.commit()

    return {"message": "Password reset successfully."}, 200
