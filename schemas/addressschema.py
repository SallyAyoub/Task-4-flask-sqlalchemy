from marshmallow import Schema, fields
class AddressSchema(Schema):
    streetAddress = fields.String()
    city = fields.String()
    state = fields.String()
    postalCode = fields.String()
