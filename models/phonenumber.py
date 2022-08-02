from database import db


class PhoneNumber(db.Model):
    __tablename__ = 'phoneNumbers'
    type = db.Column(db.String(200), nullable=False)
    number = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    phone_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return '<PhoneNumber %r>' % self.number

    def __int__(self, phone_type, phone_number):
        self.type = phone_type
        self.number = phone_number
        
