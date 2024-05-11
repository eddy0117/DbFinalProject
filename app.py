from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, redirect, request, session, jsonify
from models import db, Song, User, Playlist 
from methods import *

import os
import json
import time

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

@app.route('/search_result', methods=['POST', 'GET'])
def search_result():
    if request.method == 'GET':
        keyword = request.args.get('keyword')
        song_data = search_song(db, keyword)
        session['song_data'] = song_data

        return render_template('search_result.html', session_data=session)

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

@app.route('/addPlaylist', methods=['POST', 'GET'])
def addPlaylist():
    if request.method == 'POST':
        data = request.json
        add_playlist(db, session['userID'], data['PlaylistName'])
    return 'addPlaylist'

@app.route('/rnPlaylist', methods=['POST', 'GET'])
def rnPlaylist():
    if request.method == 'POST':
        data = request.json
        rename_playlist(db, data['PlaylistID'], data['PlaylistName'])
    return 'rnPlaylist'

@app.route('/addToPlaylist', methods=['POST', 'GET'])
def addToPlaylist():
    if request.method == 'POST':
        data = request.json
        # 判斷歌曲是否已經存在於播放清單中
        if not SongList.query.filter_by(PlaylistID=data['PlaylistID'], SongID=data['SongID']).first():
            add_song_to_playlist(db, data['PlaylistID'], data['SongID'])
            return 'success'
        return 'failed'
    
@app.route('/delSongFromPlaylist', methods=['POST', 'GET'])
def delSongFromPlaylist():
    if request.method == 'POST':
        data = request.json
        del_song_from_playlist(db, data['PlaylistID'], data['SongID'])
    return 'delSongFromPlaylist'
if __name__ == "__main__":
    
    app.run(debug=True)