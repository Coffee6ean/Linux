from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, \
                    BooleanField, RadioField, SelectField, \
                    TextAreaField
from wtforms.validators import InputRequired, Email, Optional, \
                                URL, Length, NumberRange

class AddPetForm(FlaskForm):
    """Form for adding a new pet"""

    name = StringField("Name", validators=[InputRequired(message="Name cannot be blank")])
    species = StringField("Species", validators=[InputRequired(message="Species cannot be blank")])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=50)])
    notes = TextAreaField("Comments", validators=[Optional(), Length(min=10)])

class EditPetForm(FlaskForm):
    """Form for editing an existing pet."""

    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = TextAreaField("Comments", validators=[Optional(), Length(min=10)])
    available = BooleanField("Available")