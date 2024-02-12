from sqlalchemy import ForeignKey
from .main import db
import datetime

class Feedback(db.Model):
    """Feedback Model."""

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)

    # Centralized Relationship Class - Entity
    entity = db.relationship('Entity', backref='file')
