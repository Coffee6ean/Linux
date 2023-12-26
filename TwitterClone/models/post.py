from . import db

class Post(db.Model):
    """Project Model."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    picture = db.Column(db.Text, nullable=True) 
    topics = db.Column(db.String(255), nullable=True)

    # Foreign Keys - 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'), nullable=False)

    def serialize(self):
        return f"<Project id={self.id} title={self.title} board={self.board}>"
