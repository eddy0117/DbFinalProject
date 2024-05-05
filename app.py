from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, redirect, request, session
app = Flask(__name__)
from models import db, Song, User, Playlist 
from methods import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)



@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
    
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    print(1)
    if request.method == 'POST':
        
        data = request.json
        username = data['username']
        password = data['password']
        add_user(db, username, password)
    

        print(username, password)
        return 'singup'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        
        data = request.json
        username = data['username']
        password = data['password']
        print(username, password)
        return 'login'
    #     user = User.query.filter_by(username=username).first()
    #     if user and user.password == password:
    #         session['username'] = username
    #         return redirect(url_for('dashboard'))
    #     else:
    #         return redirect(url_for('login'))
    # return render_template('login.html')
    

if __name__ == "__main__":
    
    app.run(debug=True)