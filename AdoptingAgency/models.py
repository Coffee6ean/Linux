from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS 
class Pet(db.Model):
    """Adopting Animal Model."""

    __tablename__ = 'pet'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Pet:[{self.id}, {self.name}, {self.species}, \
            {self.photo_url}, {self.age}, {self.notes}, {self.available}]>"


