from flask_wtf import FlaskForm
from wtforms import StringField, FloatField

class AddSnackForm(FlaskForm):
    """Form for adding snacks."""

    name = StringField("Snack Name")
    price = FloatField("Price in USD")