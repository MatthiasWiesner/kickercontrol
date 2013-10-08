from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.validators import Required, Email, NumberRange

class LoginForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me', default=False)

class SignupForm(Form):
    username = TextField('Username', validators=[Required()])
    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    password_confirm = PasswordField('Password Confirmation', validators=[Required()])
    remember = BooleanField('Remember me', default=False)

class GameForm(Form):
    teamA_result = IntegerField('Team A result', validators=[Required(), NumberRange(min=1, max=10)])
    teamB_result = IntegerField('Team A result', validators=[Required(), NumberRange(min=1, max=10)])
    teamA_frontend = SelectField('Team A frontend', coerce=int)
    teamA_backend = SelectField('Team A backend', coerce=int)
    teamB_frontend = SelectField('Team B frontend', coerce=int)
    teamB_backend = SelectField('Team A backend', coerce=int)
