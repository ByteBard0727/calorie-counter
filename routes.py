from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from __init__ import db
from forms import RegistrationForm, LoginForm
from models import User, UserDiet, Diet, UserExercise, UserGoal, UserWeight, Session
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from utils import get_last_login, update_session_duration, record_logout, record_login

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
            return redirect(url_for('main.api_dashboard'))
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
@main.route('/home')
def home():
    return "just testing"

#This route will be covered by front-end as it will be heavy on user interaction
@main.route('/api/dashboard', methods=['GET'])
@login_required
def api_dashboard():
    last_login = get_last_login(current_user.user_id)
    if last_login:
        return render_template('index.html', last_login)
    
    else:
        last_login = datetime.now()
        #Weight = 'Could not find prior weight records'
        #calories = 'Could not find prior Caloric intake records'

    #if user and user.Weight:
        #Weight = user.Weight
    #if user and user.calories:
        #calories = user.calories
    #current_date = datetime.now().strftime('%d-%m-%Y')
    return "Welcome! this is the first time you have logged in", render_template('index.html', last_login=last_login)

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

@main.route('/logout', methods=['POST'])
@login_required
def logout():
    record_logout()
    logout_user()
    return redirect(url_for('main.login'))