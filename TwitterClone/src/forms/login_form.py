from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import InputRequired, Email

class LoginForm(FlaskForm):
    """Form for User Log-In"""

    email = EmailField("Email", validators=[
        InputRequired(message="You missed a spot! Don't forget to add your email."), 
        Email()
    ])
    password = PasswordField("Password", validators=[
        InputRequired(message="Oops! It seems there might be an issue with the password. Please verify and try again")
    ])

    def __repr__(self):
        return f"LoginForm(email={self.email.data}, password={self.password.data})"
    