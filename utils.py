from sqlalchemy import desc, func, asc
from __init__ import db
from models import UserDiet, UserExercise, UserWeight, UserGoal, User, Session
from datetime import datetime, timedelta
from flask_login import current_user
from flask import request

# Time functions to get start and end of the period (day, week, month, year)
def get_start_and_end_of_period(period_type):
    today = datetime.now()

    if period_type == 'day':
        start_of_day = datetime(today.year, today.month, today.day, 0, 0, 0)
        end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)
        return start_of_day, end_of_day

    elif period_type == 'week':
        start_of_week = today - timedelta(days=today.weekday())  # Start of the week (Monday)
        end_of_week = start_of_week + timedelta(days=7) - timedelta(seconds=1)
        return start_of_week, end_of_week

    elif period_type == 'month':
        if today.month == 12:
            # Roll over to January of the next year
            end_of_month = datetime(today.year + 1, 1, 1, 0, 0, 0) - timedelta(seconds=1)
        else:
            # Increment the month normally
            end_of_month = datetime(today.year, today.month + 1, 1, 0, 0, 0) - timedelta(seconds=1)
        start_of_month = datetime(today.year, today.month, 1, 0, 0, 0)
        return start_of_month, end_of_month

    elif period_type == 'year':
        start_of_year = datetime(today.year, 1, 1, 0, 0, 0)
        end_of_year = datetime(today.year + 1, 1, 1, 0, 0, 0) - timedelta(seconds=1)
        return start_of_year, end_of_year

    return None, None

# Generic function to get the total calories for any period (day, week, month, year)
def get_total_consumed_calories(user_id, period_type):
    start_of_period, end_of_period = get_start_and_end_of_period(period_type)
    if start_of_period and end_of_period:
        total_calories = db.session.query(func.sum(UserDiet.caloric_value)).filter(
            UserDiet.user_id == user_id,
            UserDiet.date_eaten >= start_of_period,
            UserDiet.date_eaten <= end_of_period
        ).scalar()
        
        return total_calories if total_calories else 0
    return 0

# Generic function to count the number of records (days, weeks, months, years) with caloric input
def count_periods(user_id, period_type):
    start_of_period, end_of_period = get_start_and_end_of_period(period_type)
    if start_of_period and end_of_period:
        count = db.session.query(func.count(func.distinct(UserDiet.date_eaten))).filter(
            UserDiet.user_id == user_id,
            UserDiet.date_eaten >= start_of_period,
            UserDiet.date_eaten <= end_of_period
        ).scalar()
        
        return count if count else 0
    return 0

# Calculate the average calorie intake for the given period
def average_calories_intake(user_id, period_type):
    # Count the periods (e.g., days, weeks, etc.) with caloric intake
    count_periods_value = count_periods(user_id, period_type)
    
    if count_periods_value == 0:
        return 0

    # Get total calories consumed in the period
    total_calories = get_total_consumed_calories(user_id, period_type)
    
    # Calculate average calories for the period
    average_calories = total_calories / count_periods_value
    
    return average_calories


def get_last_login(user_id):
    login_time = db.session.query(Session.login_time).filter(
        Session.user_id == user_id
    ).order_by(desc(Session.login_time)).limit(2).all()
    return login_time[1][0] if len(login_time) > 1 else None
print(f"Last login retrieved: {get_last_login}")



#FROM THIS POINT FORWARD THE DB UPDATE SESSIONS REGARDING LOGIN AND LOGOUT ARE SPECIFIED
def update_session_duration(user_session):
   if user_session.logout_time and user_session.login_time:
    user_session.session_duration = (user_session.logout_time - user_session.login_time).total_seconds()

def record_logout(user_id):
    user_session = Session.query.filter_by(user_id=current_user.user_id).order_by(Session.login_time.desc()).first()
    if user_session:
        logout_time = datetime.now()
        update_session_duration(user_session)
        db.session.commit()

def record_login(user_id):
    # Create a new session entry for the user
    login_time = datetime.now()
    user_session = Session(
        user_id=user_id,
        login_time=login_time,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(user_session)
    db.session.commit()

