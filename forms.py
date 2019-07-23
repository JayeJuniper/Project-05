import datetime
from flask_wtf import Form
from wtforms import StringField, TextAreaField, DateTimeField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Length, EqualTo)


class EntryForm(Form):
    """EntryForm is the form used in creating journal entries."""
    title = StringField("Title", validators=[DataRequired()])
    timestamp = DateTimeField(
        "Date",
        default=datetime.datetime.now,
        validators=[DataRequired()]
        )
    time_spent = StringField(
        "Time spent",
        validators=[DataRequired()]
        )
    content = TextAreaField(
        "What did you learn?",
        validators=[DataRequired()]
        )
    resources = TextAreaField(
        "Resources you used",
        validators=[DataRequired()]
        )
    
