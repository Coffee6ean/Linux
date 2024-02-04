from ..main import db

class Picture(db.Model):
    """Model for storing user-uploaded pictures."""
    
    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)