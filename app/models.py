from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    dob = db.Column(db.String(10))  # YYYY-MM-DD
    gender = db.Column(db.String(10))
    profile_pic = db.Column(db.String(255), default='default_profile.png')
    helmets = db.relationship('Helmet', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Helmet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    helmet_id = db.Column(db.String(20), index=True, unique=True)
    helmet_name = db.Column(db.String(64))
    worker_name = db.Column(db.String(64))
    location = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # New Health & Emergency Fields
    battery_level = db.Column(db.Float, default=100.0)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    emergency_contact = db.Column(db.String(20))
    blood_group = db.Column(db.String(5))
    
    readings = db.relationship('Reading', backref='helmet', lazy='dynamic')

    def get_latest_reading(self):
        return Reading.query.filter_by(helmet_id=self.helmet_id).order_by(Reading.timestamp.desc()).first()

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    helmet_id = db.Column(db.String(20), db.ForeignKey('helmet.helmet_id'))
    temperature = db.Column(db.Float)
    gas = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
