from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

#This will be the home page
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('')

if __name__ == '__main__':
    app.run(debug=True)
