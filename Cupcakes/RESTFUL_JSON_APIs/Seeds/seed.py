import sys
sys.path.append('../')
from models import db, connect_db,  Cupcake
from app import app

def initialize_app():
    db.drop_all()
    db.create_all()

    Cupcake.query.delete()

def fill_app():
    cupcakes = [
        Cupcake(flavor='Chocolate',size='Medium',rating=4.5),
        Cupcake(flavor='Vanilla',size='Large',rating=4.2),
        Cupcake(flavor='Strawberry',size='Small',rating=4.7),
        Cupcake(flavor='Red Velvet',size='Large',rating=4.8),
        Cupcake(flavor='Lemon',size='Medium',rating=4.6),
        Cupcake(flavor='Cookies and Cream',size='Small',rating=4.9),
        Cupcake(flavor='Pistachio',size='Large',rating=4.7),
        Cupcake(flavor='Salted Caramel',size='Medium',rating=4.5),
        Cupcake(flavor='Coconut',size='Small',rating=4.3),
        Cupcake(flavor='Raspberry',size='Large',rating=4.6),
        Cupcake(flavor='Mango',size='Medium',rating=4.4),
        Cupcake(flavor='Coffee',size='Small',rating=4.8),
        Cupcake(flavor='Pumpkin Spice',size='Large',rating=4.7),
        Cupcake(flavor='Almond',size='Medium',rating=4.5),
        Cupcake(flavor='Cherry',size='Small',rating=4.2),
        Cupcake(flavor='Maple',size='Medium',rating=4.6),
        Cupcake(flavor='Blueberry',size='Medium',rating=4.4),
        Cupcake(flavor='Hazelnut',size='Small',rating=4.9)
    ]

    db.session.add_all(cupcakes)
    db.session.commit()
    
initialize_app()
fill_app()