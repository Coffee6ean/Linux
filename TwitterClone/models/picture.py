from sqlalchemy import ForeignKey, Integer, String
from .main import db

class Picture(db.Model):
    """Model for pictures."""
    __tablename__ = 'pictures'

    id = db.Column(Integer, primary_key=True)
    entity_id = db.Column(Integer, ForeignKey('entities.id'), nullable=False)
    url = db.Column(String(255), nullable=False)
    description = db.Column(String(255))

    # Define relationship with Entity model
    entity = db.relationship('Entity', backref='pictures')

    def serialize(self):
        """Serialize picture data."""
        return {
            "id": self.id,
            "entity_id": self.entity_id,
            "url": self.url,
            "description": self.description,
        }
