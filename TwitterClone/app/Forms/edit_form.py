from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, \
                    TextAreaField, DateField
from wtforms.validators import DataRequired, InputRequired, Optional, \
                                Email, Length, Regexp, URL

class EditForm(FlaskForm):
    """Form for User Log-In"""
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(max=30)
    ])
    banner = StringField('Profile Banner', validators=[Optional()])
    picture = StringField('Profile Picture', validators=[Optional()])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(), 
        Length(max=50)
    ])
    first_name = StringField('First Name', validators=[Optional(), Length(max=30)])
    sur_name = StringField('Sur Name', validators=[Optional(), Length(max=30)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=30)])
    birth_date = DateField('Birth Date', validators=[Optional(), DataRequired()])
    about = TextAreaField('About')
    pronouns = StringField('Pronouns')
    website = StringField('Website', validators=[Optional(), URL()])
    linked_in = StringField('LinkedIn', validators=[Optional(), URL()])

    def __repr__(self):
        return f"EditForm(email={self.email.data}, username={self.username.data}, " \
               f"banner={self.banner.data}, picture={self.picture.data}, " \
               f"first_name={self.first_name.data}, last_name={self.last_name.data}, " \
               f"birth_date={self.birth_date.data}, about={self.about.data}, " \
               f"pronouns={self.birth_date.data}, website={self.about.data}, " \
               f"linked_in={self.birth_date.data})" 
    