from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class DateForm(FlaskForm):
    date = StringField("Date", validators=[DataRequired()])