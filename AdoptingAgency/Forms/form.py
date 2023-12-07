from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, \
                    BooleanField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Optional

class AddAnimalForm(FlaskForm):
    """Form for adding a new animal"""

    name = StringField("Name", validators=[InputRequired(message="Name cannot be blank")])
    species = StringField("Species", validators=[InputRequired(message="Species cannot be blank")])
    photo = StringField("Photo URL")
    age = IntegerField("Age")
    notes = StringField("Notes")