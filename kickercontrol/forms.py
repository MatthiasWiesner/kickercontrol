from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, IntegerField, HiddenField
from wtforms.widgets import HiddenInput 
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
    teamBlack_result = IntegerField(widget=HiddenInput(), validators=[Required(), NumberRange(min=1, max=10)])
    teamRed_result = IntegerField(widget=HiddenInput(), validators=[Required(), NumberRange(min=1, max=10)])
    teamBlack_frontend = HiddenField(validators=[Required()])
    teamBlack_backend = HiddenField(validators=[Required()])
    teamRed_frontend = HiddenField(validators=[Required()])
    teamRed_backend = HiddenField(validators=[Required()])
