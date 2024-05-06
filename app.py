from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, redirect, request, session, jsonify
from models import db, Song, User, Playlist 
from methods import *

import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)



@app.route('/', methods=['POST', 'GET'])
def index():
    if 'isLogin' not in session:
        session['isLogin'] = False
    if session['isLogin']:
        playlist_pkg = get_user_playlist(db, session['userID'])
        session['playlist'] = playlist_pkg

    return render_template('index.html', session_data=session)

@app.route('/getSession', methods=['POST', 'GET'])
def getSession():
    return jsonify({'session': session})


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

        # 判斷使用者是否存在，並回傳使用者ID和播放清單陣列
        if is_user_exist(username, password):
            session['isLogin'] = True
            session['userID'] = is_user_exist(username, password)
            
                
            print(session)
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/deletePlaylist', methods=['POST', 'GET'])
def deletePlaylist():
    if request.method == 'POST':
        data = request.json
        del_playlist(db, data['PlaylistID'])   
    return 'deletePlaylist'
if __name__ == "__main__":
    
    app.run(debug=True)