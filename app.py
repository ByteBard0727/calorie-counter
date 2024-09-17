from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# for CSRF protection
app.config['SECRET_KEY'] = 'mew'

#config SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:<YourPassword>@localhost/calorie-counter?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#define the db
db = SQLAlchemy(app)

#define the db model this will let flask-sqlalchemy map a route to the table and the right column created in dbeaver
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
        
    def set_Password(self, password):
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)
    
    def get_id(self):
        return self.UserID
    
#define the diet table of the db and map routes to different tables and columns creating a class
class Diet(db.Model):
    __tablename__ = 'Diet'
    diet_id = db.Column(db.Integer, primary_key=True)
    proteine = db.Column(db.String)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    caloric_value = db.Column(db.Integer)

#define the diet table of the db and map routes to different tables and columns creating a class    
class Dish(db.Model):
    __tablename__ = 'Dish'
    dishid = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(100))
    total_calories = db.Column(db.Integer)

#define the UserDiet table of the db and map routes to different tables and columns creating a class
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

#defining the Weight table
class UserWeight(db.Model):
    __tablename__ = 'WeightHistory'
    weight_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    weight = db.Column(db.Float)
    date = db.Column(db.DateTime)

class UserExercise
    __tablename__ = 'Exercise'
    exercise_id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Time)
    calories_burned = db.Column(db.Integer)
    exercise_type = db.Column(db.String)
    date_performed = db.Column(db.DateTime)
    exercise_type = db.Column(db.String(100))

class UserGoal

#initialize the db
with app.app_context():
    db.create_all()

#init the loginmanager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#instructions for flasklogin to load users from dbeaver
@login_manager.user_loader
def load_user(UserID):
    return User.query.get(int(UserID))

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Username=form.Username.data).first()
        if user and user.check_password(form.Password.data):
            login_user(user)
            user.last_login = datetime.now()
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            flash('Unable to login. Check your username and password.')
    return render_template('login.html', form=form)

#Map to the register page using the forms from the imported Forms
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(Email=form.Email.data).first():
            flash('Email already registered. Please use a different one.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(form.Password.data, method='pbkdf2:sha256')
        new_user = User(Username=form.Username.data, Email=form.Email.data, Password=hashed_password, JoinDate=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#The homepage with, current date, date lastlogin and last weight/diet/
@app.route('/home')
def home():
    return f"just testing"

@app.route('/dashboard')
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
        calories = "Could not find prior Caloric intake records"
    current_date = datetime.now().strftime('%d-%m-%Y')
    return render_template('index.html', current_date=current_date, last_login=last_login, Weight=Weight, calories=calories)

@app.route('/weight_forecast', methods =['GET', 'Post'])
@login_required
def weight_forecast():
    current_user_id = UserDiet.query.filterby(UserID=current_user.UserID).first()

    
@app.route('/dish_cal_predictor', methods =['GET', 'Post'])
@login_required
def dish_cal_predictor():
    #specify the current day and store in value today
    today = datetime.now()
    #specify when the start of the day is
    start_of_day = datetime(today.year, today.month, today.day, 0, 0, 0)
    #specify the end of the day by adding 1 day to the start of the day and then subtracting 1 second to signify end of the day
    end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)
    #making sure to get the id for the current user
    current_user_id = current_user.UserID
    #asking the UserDiet table to sum all the values in the different cells filtered between the start and the end of the day 
    total_day_calories = db.session.query(db.func.sum(UserDiet.caloric_value)).filter(
        UserDiet.user_id == current_user_id,
        UserDiet.date_eaten >= start_of_day,
        UserDiet.date_eaten <= end_of_day
    ).scalar()
    if total_day_calories is None:
        total_day_calories = 0
    print(f"Total calories consumed today: {total_day_calories}")

    


#route to the calorie forecast app
@app.route('/exercise_calorie_forecast', methods =['GET', 'Post'])
@login_required
def exercise_calorie_forecast():
    current_user_id = current_user.UserID

    db.session.query(db.func.sum(UserDiet.caloric_value)).filter(
        UserDiet.UserID == current_user_id,
        UserDiet.date_eaten >= start_of_day,
        UserDiet.date_eaten <= end_of_day,
    ).scalar()



@app.route('/goal_planner', methods =['GET', 'Post'])
@login_required
def goal_planner():
    print("maintenance")




if __name__ == '__main__':
    app.run(debug=True)