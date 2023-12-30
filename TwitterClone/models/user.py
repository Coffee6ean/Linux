from sqlalchemy import Date
from .main import db, bcrypt
from .post import Post
from .board import Board
from .project import Project
from .association import user_board_association, user_project_association


class User_Profile(db.Model):
    """User Profile Model."""
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture = db.Column(db.Text, nullable=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=True)
    sur_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    birth_date = db.Column(Date, nullable=False)
    about = db.Column(db.Text, nullable=True)
    pronouns = db.Column(db.Text, nullable=True)
    website = db.Column(db.Text, nullable=True)
    linked_in = db.Column(db.Text, nullable=True)

    # Foreign Keys & Relationships - 
    posts = db.relationship('Post', backref='user')
    boards = db.relationship(
        'Board', # Related model name
        secondary=user_board_association, # Association table for many-to-many relationship
        backref='users', # Reverse relationship field on the 'Project' model
        lazy='joined', # Lazy loading strategy for the relationship
        uselist=True # Whether to use a list or a scalar for the relationship
    )
    projects = db.relationship(
        'Project', 
        secondary=user_project_association, 
        backref='users', 
        lazy='joined', 
        uselist=True
    )

    @classmethod
    def register(cls, email, username, password, birth_date):
        """Register a user."""

        hashed_pwd = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed_pwd.decode("utf8")
        new_user = cls(
            email = email,
            username = username,
            password = hashed_utf8,
            birth_date = birth_date
        )

        db.session.add(new_user)
        return new_user
    
    @classmethod
    def authenticate(cls, email, password):
        """Validate that user exists and password is correct."""
        user = User_Profile.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
        
    def serialize(self):
        return {
            "id": self.id, 
            "picture": self.picture,
            "username": self.username, 
            "password": self.password, 
            "email": self.email,
            "first_name": self.first_name,
            "sur_name": self.sur_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "about": self.about,
            "pronouns": self. pronouns,
            "website": self.website
        }
    
    def __repr__(self):
        return f"<User [ \
            id={self.id}, \
            username={self.username}, \
            firstname={self.first_name}, \
            lastname={self.last_name}, \
            password={self.password}, \
            birth_date={self.birth_date} \
            ]>"
