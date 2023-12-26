from . import db, bcrypt

class Board(db.Model):
    """Board Model."""

    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    topics = db.Column(db.Text, nullable=True)
    board = db.Column(db.Text, nullable=True)
    
    user_id = db.relationship('User', backref='projects')

    def serialize(self):
        return f"<Project id={self.id} title={self.title} board={self.board}>"
