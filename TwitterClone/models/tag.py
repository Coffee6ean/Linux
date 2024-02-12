from sqlalchemy import ForeignKey
from .main import db

class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)

    # Foreign key to link to the Entity table
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'))  
    name = db.Column(db.Text, nullable=False, unique=True)

    # Centralized Relationship Class - Entity
    entity = db.relationship('Entity', backref='tag')
