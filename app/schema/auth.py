from marshmallow import Schema, fields, validates, ValidationError


class UserRegisterSchema(Schema):
    email = fields.Email(
        required=True,
    )
    username = fields.String(required=True, validate=lambda s: len(s) >= 3)
    password = fields.String(required=True, validate=lambda p: len(p) >= 6)


class UserLoginSchema(Schema):
    email = fields.Email(
        required=True,
    )
    password = fields.String(required=True)


class PasswordResetRequestSchema(Schema):
    email = fields.Email(required=True)


class OTPVerificationSchema(Schema):
    email = fields.Email(
        required=True, error_messages={"required": "Email is required."}
    )
    otp = fields.Str(
        required=True, error_messages={"required": "OTP code is required."}
    )


class ResetPasswordSchema(Schema):
    email = fields.Email(required=True)
    otp = fields.String(
        required=True,
    )
    new_password = fields.String(required=True, validate=lambda p: len(p) >= 6)


class ChangePasswordSchema(Schema):
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True)
