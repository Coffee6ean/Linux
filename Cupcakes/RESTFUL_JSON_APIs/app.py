from flask import Flask, request, render_template, \
                    redirect, jsonify
from models import db, connect_db, Cupcake
from Keys.secrets import RESTFUL_APP_KEY

app = Flask(__name__)

app.app_context().push()

# Configure the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = RESTFUL_APP_KEY

# Connect the Flask app to the database
connect_db(app)

# ROUTES

@app.route("/")
def root():
    """Render homepage."""
    return render_template("index.html")

# Listing
@app.route('/api/cupcakes')
def list_cupcakes():
    """List all cupcakes."""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    response_json = jsonify(cupcakes=all_cupcakes)

    return response_json

# Getting
@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Get details of a specific cupcake."""
    cupcake = Cupcake.query.get_or_404(id)
    response_json = jsonify(cupcake=cupcake.serialize())

    return response_json

# Creating
@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake."""
    data = request.json

    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data['image'] or None
    )

    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())

    return (response_json, 201)

# Update
@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def edit_cupcake(id):
    """Edit details of a specific cupcake."""
    data = request.json

    edit_cupcake = Cupcake.query.get_or_404(id)
    edit_cupcake.flavor = data['flavor']
    edit_cupcake.rating = data['rating']
    edit_cupcake.size = data['size']
    edit_cupcake.image = data['image']

    db.session.add(edit_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=edit_cupcake.serialize())

    return (response_json, 200)

# Delete
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Remove a specific cupcake."""
    delete_cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(delete_cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
