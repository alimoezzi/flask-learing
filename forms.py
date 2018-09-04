from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,Length

class SignupForm(Form):
    first_name = StringField("First name",validators=[DataRequired(message="Please Enter your first name")])#make it required field
    last_name = StringField('last name',validators=[DataRequired(message="Please Enter your last name")])
    email = StringField('Email',validators=[DataRequired(message="Email is not entered"),Email("Email is not valid")])
    password = PasswordField('Password',validators=[DataRequired(message="Password at least 6 chars"),Length(min=5 , message="At least 6 characters or more")])
    submit = SubmitField('Sign up')

class LoginForm(Form):
    email = StringField('Email',validators=[DataRequired("Please enter your email address."),Email("Please eneter a valid email")])
    password = PasswordField('Password',validators=[DataRequired(message="Password at least 6 chars"),Length(min=5 , message="At least 6 characters or more")])
    submit = SubmitField('Sign in')

class AddressForm(Form):
    address = StringField('Adress',validators=[DataRequired("No place entered")])
    submit = SubmitField('Search')
