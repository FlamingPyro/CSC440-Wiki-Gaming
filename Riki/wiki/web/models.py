from .extensions import db
class ShoppingInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zipcode = db.Column(db.String(10))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))