from .extensions import db

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    comments = db.Column(db.String(500))
    numLikes = db.Column(db.Integer, default=0)
