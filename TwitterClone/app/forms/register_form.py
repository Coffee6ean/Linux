from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import InputRequired, Email, Length, Regexp

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[
        InputRequired(), 
        Email(), 
        Length(max=50)]
    )
    username = StringField("Username", validators=[
        InputRequired(message="You missed a spot! Don't forget to add your username."), 
        Length(max=30)
    ])
    password = PasswordField("Password", validators=[
        InputRequired(message="Let's set up a password for your account 😊"), 
        Length(min=6, max=20),
        Regexp(
            regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])",
            message="Password must include at least one lowercase letter, one uppercase letter, one digit, and one special character."
        )
    ])
    birth_date = DateField("Birthdate", validators=[InputRequired()])

    def __repr__(self):
        return f"SignupForm(email={self.email.data}, username={self.username.data}, " \
               f"password={self.password.data}, birth_date={self.birth_date.data})"
