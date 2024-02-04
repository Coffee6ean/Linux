from sqlalchemy import Boolean
from ..main import db

class Task(db.Model):
    """Model for storing user tasks."""
    
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    completed = db.Column(Boolean, nullable=False, default=False)
