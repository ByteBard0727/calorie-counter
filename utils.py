from app import db
from models import UserDiet, UserExercise, UserWeight, UserGoal, User
from datetime import datetime, timedelta

def get_start_and_end_of_day():
    today = datetime.now()
    start_of_day = datetime(today.year, today.month, today.day, 0, 0, 0)
    end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)
    return start_of_day, end_of_day

def get_total_day_consumed_calories(user_id):
    start_of_day, end_of_day = get_start_and_end_of_day()
    total_day_calories = db.session.query(db.func.sum(UserDiet.caloric_value)).filter(
        UserDiet.user_id == user_id,
        UserDiet.date_eaten >= start_of_day,
        UserDiet.date_eaten <= end_of_day
    ).scalar()

    if total_day_calories is None:
        total_day_calories = 0
    return total_day_calories

def get_total_week_consumed_calories(user_id):
    start_of_week, end_of_week