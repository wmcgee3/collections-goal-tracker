from flask_login import UserMixin
from datetime import date

from goal_tracker import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    records = db.relationship('Record', back_populates='user')


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_amount = db.Column(db.Float, nullable=False, default=0)
    payments = db.relationship('Payment', back_populates='record')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='records')
    month_id = db.Column(db.Integer, db.ForeignKey('month.id'))
    month = db.relationship('Month', back_populates='records')
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'))
    year = db.relationship('Year', back_populates='records')


class Month(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    records = db.relationship('Record', back_populates='month')


class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    records = db.relationship('Record', back_populates='year')


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today())
    amount = db.Column(db.Integer, nullable=False)
    collected = db.Column(db.Boolean, nullable=False, default=False)
    record_id = db.Column(db.Integer, db.ForeignKey('record.id'))
    record = db.relationship('Record', back_populates='payments')
