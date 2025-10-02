from flask import Blueprint, render_template, redirect, url_for, flash, request
from website.forms import RegisterForm, LoginForm
from website.models import User, Event
from website import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

routes = Blueprint('routes', __name__)

# Home page
@routes.route('/')
def home():
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template('index.html', events=events)


# Register page
@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('routes.register'))

        # Hash password before saving
        hashed_pw = generate_password_hash(form.password.data, method='pbkdf2:sha256')

        # Create new user
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html', form=form)



# Login page
@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Check password hash
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('routes.home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)


# Logout page
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))


@routes.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome {current_user.name}! This page is protected."

