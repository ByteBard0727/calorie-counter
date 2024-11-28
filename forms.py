from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    Username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    confirm_Password = PasswordField('confirm_Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    Username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    Password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class FoodForm(FlaskForm):
    print("maintenance")
class ExcerciseForm(FlaskForm):
    print("maintenance")
class GoalForm(FlaskForm):
    print("maintenance")