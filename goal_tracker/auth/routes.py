from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from datetime import date

from goal_tracker.auth.forms import LoginForm
from goal_tracker.models import User, Record, Month, Year
from goal_tracker import bcrypt, db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('You are now logged in.', 'success')
            todays_date = date.today()
            if todays_date.month == 12:
                next_month_date = todays_date.replace(
                    month=1, year=todays_date.year+1)
            else:
                next_month_date = todays_date.replace(
                    month=todays_date.month+1)
            if not Record.query.filter_by(user_id=current_user.id).filter(Record.month.has(number=todays_date.month)).filter(Record.year.has(number=todays_date.year)).scalar():
                month = db.session.query(Month).filter_by(number=todays_date.month).first()
                year = db.session.query(Year).filter_by(number=todays_date.year).first()
                if not year:
                    year = Year(
                        number=todays_date.year
                    )
                    db.session.add(year)
                    db.session.commit()
                new_this_month_record = Record(
                    user=current_user,
                    month=month,
                    year=year
                )
                db.session.add(new_this_month_record)
                db.session.commit()
            if not Record.query.filter_by(user_id=current_user.id).filter(Record.month.has(number=next_month_date.month)).filter(Record.year.has(number=next_month_date.year)).scalar():
                next_month = Month.query.filter_by(number=next_month_date.month).first()
                next_year = Year.query.filter_by(number=next_month_date.year).first()
                if not next_year:
                    next_year = Year(
                        number=next_month_date.year
                    )
                    db.session.add(next_year)
                    db.session.commit()
                new_next_month_record = Record(
                    user=current_user,
                    month=next_month,
                    year=next_year
                )
                db.session.add(new_next_month_record)
                db.session.commit()
            record = Record.query.filter_by(user_id=current_user.id).filter(Record.month.has(number=todays_date.month)).filter(Record.year.has(number=todays_date.year)).first()
            return redirect(url_for('record.show_record', record_id=record.id))
        else:
            flash('Login unsuccessful.', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out.', 'success')
    return redirect(url_for('auth.login'))
