from ..main import db

class File(db.Model):
    """Model for storing user-uploaded files."""
    
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
