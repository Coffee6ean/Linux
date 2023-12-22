from . import db

class Project(db.Model):
    """Project Model."""

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.Text, nullable=True)
    topics = db.Column(db.Text, nullable=True)
    board = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref='projects')

    def serialize(self):
        return f"<Project id={self.id} title={self.title} board={self.board}>"
