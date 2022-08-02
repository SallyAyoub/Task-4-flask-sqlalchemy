from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.relationship('Address', backref='user_address', cascade="all,delete", lazy=True, uselist=False, )
    phoneNumbers = db.relationship('PhoneNumber', backref='user_phone', cascade="all,delete", uselist=False)

    def __repr__(self):
        return '<User %r>' % self.firstName




