from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, redirect, request, session, Response, jsonify
from flask_socketio import SocketIO, emit
from models import db, Song, User, Playlist 
from methods import *

import os
import json
import time
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

db.init_app(app)

TOP_N = 10

# admin

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    top_data = {}
    if request.method == 'GET':
        if session['isLogin'] == True and session['userID'] == 0:
            top_data['top_n_songs_data'] = get_topN_famous_song(TOP_N)
            top_data['top_n_albums_data'], top_data['top_n_albums_Pcount'] = get_topN_famous_album(TOP_N)
            top_data['top_n_artists_data'], top_data['top_n_artists_Pcount'], top_data['top_n_artists_name'] = get_topN_famous_artist(TOP_N)
            return render_template('dashboard.html', session_data=session, top_data=top_data)
        else:
            return redirect('/')
        
@app.route('/admin_search_result', methods=['POST', 'GET'])
def admin_search_result():
    if request.method == 'GET':
        keyword = request.args.get('keyword')
        song_data = search_song(db, keyword)
        session['song_data'] = song_data
        if session['isLogin'] == True and session['userID'] == 0:
            return render_template('admin_search_result.html', session_data=session)
        else:
            return redirect('/')
        
@app.route('/addSong', methods=['POST', 'GET'])
def addSong():
    if request.method == 'POST':
        data = request.json
        data['ArtistName'] = data['ArtistName'].split(',')
        add_song(db, data['Title'], data['Album'], data['ReleaseYear'], data['Duration'], data['PictureSrc'], data['SongSrc'], *data['ArtistName'])
    return 'addSong'

@app.route('/delSong', methods=['POST', 'GET'])
def delSong():
    if request.method == 'POST':
        data = request.json
        del_song(db, data['SongID'])
    return 'delSong'

# normal user

@app.route('/', methods=['POST', 'GET'])
def index():
    top_data = {}
    if 'isLogin' not in session:
        session['isLogin'] = False
    elif session['isLogin']:
         # 將熱門歌曲系列存入session會導致session過大，因此存入top_data不根據用戶而是全域
        
        playlist_pkg = get_user_playlist(db, session['userID'])
        session['playlist'] = playlist_pkg
        top_data['top_n_songs_data'] = get_topN_famous_song(TOP_N)
        top_data['top_n_albums_data'], top_data['top_n_albums_Pcount'] = get_topN_famous_album(TOP_N)
        top_data['top_n_artists_data'], top_data['top_n_artists_Pcount'], top_data['top_n_artists_name'] = get_topN_famous_artist(TOP_N)
    return render_template('index.html', session_data=session, top_data=top_data)



@app.route('/getSession', methods=['POST', 'GET'])
def getSession():
    return jsonify({'session': session})

@app.route('/search_result', methods=['POST', 'GET'])
def search_result():
    if request.method == 'GET':
        session.pop('top_n_songs_data', None)
        session.pop('top_n_albums_data', None)
        keyword = request.args.get('keyword')
        song_data = search_song(db, keyword)
        session['song_data'] = song_data
        if 'isLogin' not in session.keys() or not session['isLogin']:
            return redirect('/')  
        else:
            return render_template('search_result.html', session_data=session)
        



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        
        data = request.json
        username = data['username']
        password = data['password']
        Gender = data['Gender']

        add_user(db, username, password, Gender)
    
        return 'singup'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        
        data = request.json
        username = data['username']
        password = data['password']
        print(username, password)
        # 判斷使用者是否存在，並回傳使用者ID和播放清單陣列
        if username == 'admin' and password == 'password':
            print('admin')
            session['isLogin'] = True
            session['userID'] = 0
            session['username'] = username
            return jsonify({'message': 'admin'})
        
        elif is_user_exist(username, password):
            session['isLogin'] = True
            session['userID'] = is_user_exist(username, password)
            session['username'] = username    
            return jsonify({'message': 'Login successful'})
        
        else:

            return jsonify({'message': 'Invalid username or password'}), 401
        
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect('/')

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

@socketio.on('stream_audio')
def stream_audio(data):

    userID = session['userID']
    user = User.query.filter_by(UserID=userID).first()
    song = Song.query.filter_by(SongID=data['SongID']).first()
    if user.Gender == 'male':
        song.PMale += 1
        db.session.commit()
    else:
        song.PFemale += 1
        db.session.commit()

    
    
    path = 'Z:/eddy/電腦/Not All Purchased Music (some form copy)/' + data['filename']
    chunk_size = 2048000
   
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                emit('audio_chunk', 'end')  
                break
            chunk_b64 = base64.b64encode(chunk).decode('utf-8')
     
            emit('audio_chunk', chunk_b64)

if __name__ == "__main__":
    
    # app.run(debug=True)
    socketio.run(app, debug=True, host='192.168.2.107')