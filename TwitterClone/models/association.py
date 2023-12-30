# models/association.py
from .main import db

user_board_association = db.Table(
    'user_board_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('board_id', db.Integer, db.ForeignKey('boards.id'))
)

user_project_association = db.Table(
    'user_project_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'))
)
