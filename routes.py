from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from __init__ import db
from forms import RegistrationForm, LoginForm
from models import User, UserDiet
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Username=form.Username.data).first()
        if user and user.check_password(form.Password.data):
            login_user(user)
            user.last_login = datetime.now()
            db.session.commit()
            return redirect(url_for('main.dashboard'))
        else:
            flash('Unable to login. Check your username and password.')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(Email=form.Email.data).first():
            flash('Email already registered. Please use a different one.')
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(form.Password.data, method='pbkdf2:sha256')
        new_user = User(Username=form.Username.data, Email=form.Email.data, Password=hashed_password, JoinDate=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/home')
def home():
    return "just testing"

@main.route('/dashboard')
@login_required
def dashboard():
    user = User.query.filter_by(UserID=current_user.UserID).first()

    if user and user.last_login:
        last_login = user.last_login.strftime('%d-%m-%Y %H:%M:%S')
    else:
        last_login = "Welcome! this is the first time you have logged in"
    Weight = "Could not find prior weight records"
    calories = "Could not find prior Caloric intake records"
    if user and user.Weight:
        Weight = user.Weight
    if user and user.calories:
        calories = user.calories
    current_date = datetime.now().strftime('%d-%m-%Y')
    return render_template('index.html', current_date=current_date, last_login=last_login, Weight=Weight, calories=calories)

@main.route('/weight_forecast', methods=['GET', 'POST'])
@login_required
def weight_forecast():
    current_user_id = current_user.UserID
    # Add logic here

@main.route('/dish_cal_predictor', methods=['GET', 'POST'])
@login_required
def dish_cal_predictor():
    today = datetime.now()
    start_of_day = datetime(today.year, today.month, today.day, 0, 0, 0)
    end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)
    current_user_id = current_user.UserID
    total_day_calories = db.session.query(db.func.sum(UserDiet.caloric_value)).filter(
        UserDiet.user_id == current_user_id,
        UserDiet.date_eaten >= start_of_day,
        UserDiet.date_eaten <= end_of_day
    ).scalar() or 0
    print(f"Total calories consumed today: {total_day_calories}")

@main.route('/exercise_calorie_forecast', methods=['GET', 'POST'])
@login_required
def exercise_calorie_forecast():
    current_user_id = current_user.UserID
    # Add logic here

@main.route('/goal_planner', methods=['GET', 'POST'])
@login_required
def goal_planner():
    print("maintenance")
