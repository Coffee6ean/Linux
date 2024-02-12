from sqlalchemy import ForeignKey, Integer, Boolean, \
                        Text
from .main import db
import datetime

class Task(db.Model):
    """Model for storing entity tasks."""
    
    __tablename__ = 'tasks'

    id = db.Column(Integer, primary_key=True)

    # Foreign key to link to the Entity table
    entity_id = db.Column(Integer, ForeignKey('entities.id'))  
    task_description = db.Column(Text)
    completed = db.Column(Boolean)

    # Define the relationship with the Entity model
    entity = db.relationship('Entity', backref='tasks')

    def serialize(self):
        return {
            "id": self.id,
            "entity_id": self.entity_id,
            "task_description": self.task_description,
            "completed": self.completed,
        }

