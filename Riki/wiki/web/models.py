from .extensions import db

class Destiny(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    comments = db.Column(db.String(500))
    numLikes = db.Column(db.Integer, default=0)

class LethalCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    comments = db.Column(db.String(500))
    numLikes = db.Column(db.Integer, default=0)

class Minecraft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    comments = db.Column(db.String(500))
    numLikes = db.Column(db.Integer, default=0)

class Tekken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    comments = db.Column(db.String(500))
    numLikes = db.Column(db.Integer, default=0)

class EldenRing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    comments = db.Column(db.String(500))
    numLikes = db.Column(db.Integer, default=0)

class Palworld(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    comments = db.Column(db.String(500))
    numLikes = db.Column(db.Integer, default=0)

class HorizonForbiddenWest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    comments = db.Column(db.String(500))
    numLikes = db.Column(db.Integer, default=0)

class Helldivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    comments = db.Column(db.String(500))
    numLikes = db.Column(db.Integer, default=0)

class ShoppingInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    zipcode = db.Column(db.String(10))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))

class HomeDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(10), nullable=False)
