from ..main import db

class Link(db.Model):
    """Model for storing user-uploaded links."""
    
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)