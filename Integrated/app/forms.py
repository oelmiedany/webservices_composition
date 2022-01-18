from flask_wtf import FlaskForm
from wtforms import TextField, SelectField, PasswordField, StringField, DateTimeField
from wtforms.validators import DataRequired


class DateForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
