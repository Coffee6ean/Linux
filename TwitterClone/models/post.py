from sqlalchemy import ForeignKey
from .main import db
import datetime

class Post(db.Model):
    """Blog Post Model."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Foreign key to link to the Entity table
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'))  
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    picture = db.Column(db.Text, nullable=True) 
    topic = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)

    # Centralized Relationship Class - Entity
    entity = db.relationship('Entity', backref='post')

    def serialize(self):
        return f"<Project id={self.id} title={self.title} board={self.boards}>"
