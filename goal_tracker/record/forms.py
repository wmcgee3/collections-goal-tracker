from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, FloatField, SubmitField
from wtforms.validators import DataRequired


class GoalForm(FlaskForm):
    goal = FloatField('Goal Amount', validators=[DataRequired()])
    submit = SubmitField('Update')


class PaymentForm(FlaskForm):
    payment = FloatField('Payment', validators=[DataRequired()])
    collected = BooleanField('Collected', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    add = SubmitField('Add')
