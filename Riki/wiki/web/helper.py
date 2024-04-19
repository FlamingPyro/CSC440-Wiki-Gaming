from .extensions import db

def increment_likes(item_id, db_model):
    item = db_model.query.get(item_id)
    if item:
        item.numLikes += 1
        db.session.commit()

