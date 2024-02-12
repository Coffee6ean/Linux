from sqlalchemy import ForeignKey, Integer, Text
from .main import db

class Link(db.Model):
    """Model for storing entity-uploaded links."""
    
    __tablename__ = 'links'

    id = db.Column(Integer, primary_key=True)
    
    # Foreign key to link to the Entity table
    entity_id = db.Column(Integer, ForeignKey('entities.id'))  
    url = db.Column(Text)
    description = db.Column(Text)

    # Define the relationship with the Entity model
    entity = db.relationship('Entity', backref='links')

    def serialize(self):
        return {
            "id": self.id,
            "entity_id": self.entity_id,
            "url": self.url,
            "description": self.description,
        }
    