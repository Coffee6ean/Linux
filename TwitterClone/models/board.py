from .main import db, bcrypt
from .association import user_board_association

class Board(db.Model):
    """Board Model."""

    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    topic = db.Column(db.Text, nullable=True)
    board = db.Column(db.Text, nullable=True)
    
    # Foreign Keys & Relationships - 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def serialize(self):
        return f"<Project id={self.id} title={self.title} board={self.board}>"
