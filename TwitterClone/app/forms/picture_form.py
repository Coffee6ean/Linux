from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField
from wtforms.validators import InputRequired

class PictureForm(FlaskForm):
    """Form for uploading pictures"""

    image = FileField("Image File", validators=[
        InputRequired(message="Please select an image file"),
        FileAllowed(['jpg', 'jpeg', 'png'], message="Only JPG, JPEG, and PNG files are allowed")
    ])
    #image_url = StringField("Image URL")
    description = StringField("Description")

    def __repr__(self):
        return f"PictureForm(image={self.image.data}, description={self.description.data})"
