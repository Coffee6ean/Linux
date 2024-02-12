from sqlalchemy import Integer, String, Text
from .main import db
import datetime

class Project(db.Model):
    """Project Model."""

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    topic = db.Column(db.Text, nullable=True)
    board = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now) 
    tags = ['project']

    # Centralized Relationship Class - Entity
    entities = db.relationship('Entity', backref='project_related_entities')

    def serialize(self):
        return f"<Project id={self.id} title={self.title} board={self.board}>"
