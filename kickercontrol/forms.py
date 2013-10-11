from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, IntegerField, HiddenField
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
    teamBlack_result = IntegerField('Team Black result', validators=[Required(), NumberRange(min=1, max=10)])
    teamRed_result = IntegerField('Team Red result', validators=[Required(), NumberRange(min=1, max=10)])
    teamBlack_frontend = HiddenField()
    teamBlack_backend = HiddenField()
    teamRed_frontend = HiddenField()
    teamRed_backend = HiddenField()
