from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#config SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:<YourPassword>@localhost/calorie-counter?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#define the db
db = SQLAlchemy

#The homepage with, current date, date lastlogin and last weight/diet/
@app.route('/home')
def home():
    current_date = datetime.now() .strftime('%d-%m-%Y')
    last_login = 

    last_weight = 
    last_diet =
    return render_template('index.html', current_date=current_date')

if __name__ == '__main__':
    app.run(debug=True)