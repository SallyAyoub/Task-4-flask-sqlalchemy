from marshmallow import Schema, fields
class PhoneNumbersSchema(Schema):
    type = fields.String()
    number = fields.String()
