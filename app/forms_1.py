from flask_wtf import FlaskForm # FlaskForm is a class that represents a form
from wtforms import StringField, PasswordField, SubmitField #StringField, PasswordField, and SubmitField are classes that represent form fields
from wtforms.validators import DataRequired, Email, EqualTo, Length #DataRequired, Email, EqualTo, and Length are classes that represent form validators

class RegistrationForm(FlaskForm): #RegistrationForm is a class that represents a form
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)]) #StringField is a class that represents a form field
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)]) 
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    submit = SubmitField('Register') #SubmitField is a class that represents a submit button

class LoginForm(FlaskForm): #LoginForm is a class that represents a form
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[DataRequired()]) 
    submit = SubmitField('Login') 