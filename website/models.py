from datetime import datetime
from flask_login import UserMixin
from website import db

# ---------- User ----------
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    # store hashed password (pbkdf2:sha256)
    password = db.Column(db.String(255), nullable=False)

    # optional relationships (safe to keep)
    events = db.relationship('Event', backref='owner', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

# ---------- Event ----------
class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    capacity = db.Column(db.Integer, nullable=False, default=50)
    tickets_sold = db.Column(db.Integer, nullable=False, default=0)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    bookings = db.relationship('Booking', backref='event', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='event', lazy=True, cascade="all, delete-orphan")

    @property
    def status(self):
        if self.tickets_sold >= self.capacity:
            return "Sold Out"
        if self.date < datetime.utcnow():
            return "Inactive"
        return "Open"

    def __repr__(self):
        return f"<Event {self.title}>"

# ---------- Booking ----------
class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    booked_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

# ---------- Comment ----------
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
