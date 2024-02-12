from sqlalchemy import Date
from .main import db, bcrypt

# User Specific Tables
from .file import File
from .task import Task
from .link import Link

# Tables
from .entity import Entity

DEFAULT_PROFILE_BANNER = 'https://img.freepik.com/fotos-premium/vista-superior-do-local-de-trabalho-elegante-escuro-com-smartphone-e-material-de-escritorio_67155-2963.jpg?w=996'
DEFAULT_USER_PICTURE = 'https://e7.pngegg.com/pngimages/419/473/png-clipart-computer-icons-user-profile-login-user-heroes-sphere-thumbnail.png'

class User_Profile(db.Model):
    """User Profile Model."""
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    banner = db.Column(db.Text, nullable=True, default=DEFAULT_PROFILE_BANNER)
    picture = db.Column(db.Text, nullable=True, default=DEFAULT_USER_PICTURE)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    role = db.Column(db.String(20))  
    profession = db.Column(db.String(50)) 
    first_name = db.Column(db.String(30), nullable=True)
    sur_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    birth_date = db.Column(Date, nullable=False)
    about = db.Column(db.Text, nullable=True)
    pronouns = db.Column(db.Text, nullable=True)
    website = db.Column(db.Text, nullable=True)
    linked_in = db.Column(db.Text, nullable=True)
    tags = ['user']

    # Centralized Relationship Class - Entity
    entities = db.relationship('Entity', backref='user_related_entities')

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

        if user and bcrypt.check_password_hash(user.password, str(password)):
            return user
        else:
            return False
        
    def serialize(self):
        return {
            "id": self.id, 
            "banner": self.banner,
            "picture": self.picture,
            "username": self.username, 
            "password": self.password, 
            "email": self.email,
            "first_name": self.first_name,
            "sur_name": self.sur_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "about": self.about,
            "pronouns": self.pronouns,
            "website": self.website,
            "linked_in": self.linked_in,
            "role": self.role,
            "profession": self.profession
        }
    
    def __repr__(self):
        return f"<User [id={self.id}, username={self.username}, firstname={self.first_name}, lastname={self.last_name}, password={self.password}, birth_date={self.birth_date}]>"
