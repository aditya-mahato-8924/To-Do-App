from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired(), Length(8)])
    submit = SubmitField('Login')

class Task(FlaskForm):
    enter_task = StringField('Enter_Task', validators=[DataRequired()])
    submit = SubmitField('Add Task')