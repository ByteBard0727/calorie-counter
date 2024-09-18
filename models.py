from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    UserID = db.Column(db.Integer, primary_key=True)
    last_login = db.Column(db.DateTime)
    Weight = db.Column(db.Float)
    JoinDate = db.Column(db.DateTime, default=datetime.now)
    calories = db.Column(db.Integer)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
        
    def set_password(self, password):
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)
    
    def get_id(self):
        return self.UserID

class Diet(db.Model):
    __tablename__ = 'Diet'
    diet_id = db.Column(db.Integer, primary_key=True)
    proteine = db.Column(db.String)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    caloric_value = db.Column(db.Integer)

class Dish(db.Model):
    __tablename__ = 'Dish'
    dishid = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(100))
    total_calories = db.Column(db.Integer)

class UserDiet(db.Model):
    __tablename__ = 'UserDiet'
    user_diet_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    diet_id = db.Column(db.Integer, db.ForeignKey('Dish.dishid'))
    date_eaten = db.Column(db.DateTime)
    fat = db.Column(db.String(20))
    vegetable = db.Column(db.String(20))
    carbs = db.Column(db.String(20))
    portionsize = db.Column(db.Float)
    caloric_value = db.Column(db.Integer)
    proteine = db.Column(db.Float)

    user = db.relationship('User', backref='user_diets')

class UserWeight(db.Model):
    __tablename__ = 'WeightHistory'
    weight_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    weight = db.Column(db.Float)
    date = db.Column(db.DateTime)

class UserExercise(db.Model):
    __tablename__ = 'Exercise'
    exercise_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    duration = db.Column(db.Time)
    calories_burned = db.Column(db.Integer)
    exercise_type = db.Column(db.String)
    date_performed = db.Column(db.DateTime)

class UserGoal(db.Model):
    __tablename__ = 'Goal'
    goal_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    goal_type = db.Column(db.String(100))
    target_value = db.Column(db.Float)
    target_date = db.Column(db.DateTime)
