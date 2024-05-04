from models import db,  Song, User, Playlist, Artist, SongList
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import time
# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


def add_song(db : SQLAlchemy, Title, Album, ReleaseYear, Duration, *ArtistName):
    song = Song(Title=Title, Album=Album, ReleaseYear=ReleaseYear, Duration=Duration)
    db.session.add(song)
    db.session.commit()
  
    for name in ArtistName:
        artist = Artist(SongID=song.SongID, Name=name)
        db.session.add(artist)
 
    db.session.commit()

def del_song(db : SQLAlchemy, SongID):
    artist = Artist.query.filter_by(SongID=SongID)
    for it in artist:
        db.session.delete(it)

    song = Song.query.filter_by(SongID=SongID).first()
    db.session.delete(song)
    db.session.commit()

def add_user(db : SQLAlchemy, username, password):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    user = User(username=username, password=password, RegistrationDate=current_time)
    db.session.add(user)
    db.session.commit()

def add_playlist(db : SQLAlchemy, username):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    playlist = Playlist(username=username, CreationDate=current_time)
    db.session.add(playlist)
    db.session.commit()

def del_playlist(db : SQLAlchemy, PlaylistID):
    songlist = SongList.query.filter_by(PlaylistID=PlaylistID)
    for it in songlist:
        db.session.delete(it)

    playlist = Playlist.query.filter_by(PlaylistID=PlaylistID).first()
    db.session.delete(playlist)
    db.session.commit()

def add_song_to_playlist(db : SQLAlchemy, PlaylistID, SongID):
    song = SongList(PlaylistID=PlaylistID, SongID=SongID)
    db.session.add(song)
    db.session.commit()

def del_song_from_playlist(db : SQLAlchemy, PlaylistID, SongID):
    song = SongList.query.filter_by(PlaylistID=PlaylistID, SongID=SongID).first()
    db.session.delete(song)
    db.session.commit()