from flask import Blueprint, render_template
from flask_login import current_user, login_required

from goal_tracker import db
from goal_tracker.models import Record

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    records_dict = {}
    records = db.session.query(Record).filter_by(user_id=current_user.id)
    for record in records:
        records_dict[str(record.id)] = {
            'year': str(record.year.number),
            'month': record.month.name,
            'goal amount': str(record.goal_amount)
        }
    return render_template('home.html', records_dict=records_dict)
