from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from __init__ import db
from forms import RegistrationForm, LoginForm
from models import User, UserDiet, Diet, UserExercise, UserGoal, UserWeight, Session
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from utils import get_last_login, update_session_duration, record_logout, record_login, average_calories_intake, get_start_and_end_of_period

main = Blueprint('main', __name__)

#first checking the user name by querying the User table searching for their username.
#then completing the password checksum. If both are true continue if one is false flashcard unable to login
#record the current login time storing it in 'login_time'
#add a new entry in the Session table /record user_id, login_time, ip_address, user_agent
#lastly update the 
@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Username=form.Username.data).first()
        if user and user.check_password(form.Password.data):
            login_user(user)
            record_login(user.user_id)
            return redirect(url_for('main.home'))
        else:
            flash('Unable to login. Check your username and password.')
    return render_template('login.html', form=form)

#Will stay on flask back-end for robust security
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

#This route will be covered by front-end as it will be heavy on user interaction
@main.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('homepage.html')

#this route will be covered by 
@main.route('/api/dashboard', methods=['GET'])
@login_required
def api_dashboard():
    # Get the last login information
    last_login = get_last_login(current_user.user_id)
    if not last_login:
        last_login = datetime.now()

    # Debugging
    print(f"Last login: {last_login}")

    # Ensure last_login is a valid datetime object
    if not isinstance(last_login, datetime):
        try:
            last_login = datetime.strftime(last_login, "%Y-%m-%d %H:%M:%S")  # Adjust format if needed
        except ValueError as e:
            print(f"Error parsing last_login: {e}")
            last_login = datetime.now()

    # Fetch average caloric intake data
    user_id = current_user.user_id
    average_calories_today = average_calories_intake(user_id, 'day')
    average_calories_this_week = average_calories_intake(user_id, 'week')
    average_calories_this_month = average_calories_intake(user_id, 'month')
    average_calories_this_year = average_calories_intake(user_id, 'year')

    # Render the dashboard template with all required data
    return render_template(
        'dashboard.html',
        last_login=last_login,
        today_avg=average_calories_today,
        week_avg=average_calories_this_week,
        month_avg=average_calories_this_month,
        year_avg=average_calories_this_year
    )

#This forecast will stay in the back-end and will be handled by flask since it is heave on computation
@main.route('/weight_forecast', methods=['GET', 'POST'])
@login_required
def weight_forecast():
    current_user_id = current_user.user_id
    # Add logic here

#Heavy on user interaction will be on the frontend
@main.route('/api/dish_cal_predictor', methods=['GET'])
@login_required
def dish_cal_predictor():
    today = datetime.now()
    start_of_day = datetime(today.year, today.month, today.day, 0, 0, 0)
    end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)
    current_user_id = current_user.user_id
    total_day_calories = db.session.query(db.func.sum(UserDiet.caloric_value)).filter(
        UserDiet.user_id == current_user_id,
        UserDiet.date_eaten >= start_of_day,
        UserDiet.date_eaten <= end_of_day
    ).scalar() or 0
    print(f"Total calories consumed today: {total_day_calories}")

#Heavy on calculations will be on backend
@main.route('/exercise_calorie_forecast', methods=['GET', 'POST'])
@login_required
def exercise_calorie_forecast():
    current_user_id = current_user.user_id
    return 'maintenance'
    # Add logic here

#Heavy on user interaction will be on the frontend
@main.route('/goal_planner', methods=['GET', 'POST'])
@login_required
def goal_planner():
    return 'maintenance'

#Will remain on the backend since no user interaction
@main.route('/logout', methods=['POST'])
@login_required
def logout():
    record_logout()
    logout_user()
    return redirect(url_for('main.login'))