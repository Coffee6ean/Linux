from sqlalchemy import ForeignKey, Integer, String, \
                        Text, DateTime
from .main import db

# Import Project class before setting up the relationship in the Entity class
from .project import Project

class Entity(db.Model):
    """Generic entity model."""

    __tablename__ = 'entities'

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('users.id'))  # Foreign key to link to the user who created the entity
    project_id = db.Column(Integer, ForeignKey('projects.id'))  # Foreign key to link to the project associated with the entity
    board_id = db.Column(Integer, ForeignKey('boards.id'))  # Foreign key to link to the board associated with the entity
    type = db.Column(String(50), nullable=False)  # Type of the entity (e.g., picture, file, task, link)
    name = db.Column(String(255))  # Name of the entity (optional)
    content = db.Column(Text)  # Content of the entity (optional)
    picture = db.Column(Text)  # Picture URL of the entity (optional)
    topic = db.Column(String(255))  # Topic of the entity (optional)
    created_at = db.Column(DateTime, default=db.func.current_timestamp(), nullable=False)

    # Relationships
    user = db.relationship('User_Profile', backref='associated_entities')  # Relationship with the User_Profile model
    project = db.relationship('Project', backref='associated_entities')  # Relationship with the Project model
    board = db.relationship('Board', backref='associated_entities')  # Relationship with the Board model

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "board_id": self.board_id,
            "type": self.type,
            "name": self.name,
            "content": self.content,
            "picture": self.picture,
            "topic": self.topic,
            "created_at": self.created_at,
        }
