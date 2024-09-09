from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mew'  # For CSRF protection

#config SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:<YourPassword>@localhost/calorie-counter?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#define the db
db = SQLAlchemy(app)

#define the db model this will let flask-sqlalchemy map a route to the table and the right column created in dbeaver
class User(db.Model):
    __tablename__ = 'User'
    UserID = db.Column(db.Integer, primary_key=True)
    last_login = db.Column(db.DateTime)
    weight = db.Column(db.Float)
    calories = db.Column(db.Integer)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(128))
    Email = db.Column(db.String(255), unique=True, nullable=False)

    def set_Password(self, password):
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)

#initialize the db
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('home')
    return render_template('login.html', form=form)

#Map to the register page using the forms from the imported Forms
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email is already registered
        if User.query.filter_by(Email=form.Email.data).first():
            flash('Email already registered. Please use a different one.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(form.Password.data, method='pbkdf2:sha256')
        new_user = User(Username=form.Username.data, Email=form.Email.data, Password=hashed_password, JoinDate=JoinDate.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#The homepage with, current date, date lastlogin and last weight/diet/
@app.route('/home')
def home():
    User = User.query.first()

    if User and User.last_login:
        last_login = User.last_login.strftime('%d-%m-%Y %H:%M:%S')
    else:
        last_login = "Welcome! this is the first time you have logged in"

    current_date = datetime.now().strftime('%d-%m-%Y')

    return render_template('index.html', current_date=current_date, last_login=last_login)

if __name__ == '__main__':
    app.run()