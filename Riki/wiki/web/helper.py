from .models import Comments
from .extensions import db

def increment_likes(item_id):
    item = Comments.query.get(item_id)
    if item:
        item.numLikes += 1
        db.session.commit()

