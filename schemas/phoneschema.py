from marshmallow import Schema, fields
class phoneNumbersSchema(Schema):
    type = fields.String()
    number = fields.String()
