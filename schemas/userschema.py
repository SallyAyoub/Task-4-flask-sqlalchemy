from schemas.addressschema import AddressSchema
from schemas.phoneschema import PhoneNumbersSchema
from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Integer()
    firstName = fields.String()
    lastName = fields.String()
    gender = fields.String()
    age = fields.Integer()
    address = fields.Nested(AddressSchema)
    phoneNumbers = fields.Nested(PhoneNumbersSchema)
