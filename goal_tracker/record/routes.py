from flask import Blueprint, render_template
from flask_login import login_required
from datetime import date

from goal_tracker import db
from goal_tracker.models import Record
from goal_tracker.record.forms import GoalForm, PaymentForm

record = Blueprint('record', __name__)


@record.route('/<int:record_id>', methods=['GET', 'POST'])
@login_required
def show_record(record_id):
    goal_form = GoalForm()
    payment_form = PaymentForm()
    record = db.session.query(Record).filter_by(id=record_id).first()
    goal_form.goal.data = record.goal_amount
    payment_form.date.data = date.today()
    return render_template(
        'show_record.html',
        goal_form=goal_form,
        expected_form=payment_form
    )
