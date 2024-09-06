from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

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

#initialie the db
with app.app_context():
    db.create_all()

#The homepage with, current date, date lastlogin and last weight/diet/
@app.route('/')
def home():
    user = User.query.first()

    if user and user.last_login:
        last_login = user.last_login.strftime('%d-%m-%Y %H:%M:%S')
    else:
        last_login = None

    current_date = datetime.now().strftime('%d-%m-%Y')

    return render_template('index.html', current_date=current_date, last_login=last_login)

if __name__ == '__main__':
    app.run()