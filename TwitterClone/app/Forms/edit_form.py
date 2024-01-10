from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, \
                    TextAreaField, DateField
from wtforms.validators import DataRequired, InputRequired, Email, \
                                Length

class EditForm(FlaskForm):
    """Form for User Log-In"""
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    banner = StringField('Banner')
    picture = StringField('Picture')
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[Length(max=30)])
    sur_name = StringField('Sur Name', validators=[Length(max=30)])
    last_name = StringField('Last Name', validators=[Length(max=30)])
    birth_date = DateField('Birth Date', validators=[DataRequired()])
    about = TextAreaField('About')
    pronouns = StringField('Pronouns')
    website = StringField('Website')
    linked_in = StringField('LinkedIn')

    def __repr__(self):
        return f"LoginForm(email={self.email.data}, password={self.password.data})"
    