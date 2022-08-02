from database import db


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    streetAddress = db.Column(db.String(400), nullable=False)
    city = db.Column(db.String(250), nullable=False)
    state = db.Column(db.String(250), nullable=False)
    postalCode = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Address %r>' % self.id

    def __int__(self, streetaddress, city, state, postalcode):
        self.streetAddress = streetaddress
        self.city = city
        self.state = state
        self.postalCode = postalcode
