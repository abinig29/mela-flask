from marshmallow import Schema, fields, validate


class CompanySchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=100))
    email = fields.Email(required=False, allow_none=True)
    website = fields.String(
        required=False, validate=validate.Length(max=100), allow_none=True
    )
    location = fields.String(
        required=False, validate=validate.Length(max=100), allow_none=True
    )
