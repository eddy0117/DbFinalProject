from models import db,  Song, User, Playlist, Artist, SongList
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import time
# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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

def search_song(db : SQLAlchemy, searchQuery):
    song = Song.query.filter(Song.Title.ilike(f'%{searchQuery}%')).all()
    song_query = []
    for it in song:
        song_data = to_dict(it)
        
        artist = Artist.query.filter_by(SongID=it.SongID)
        song_data['Artist'] = artist[0].Name
        for art in artist[1:]:
            song_data['Artist'] += f', {art.Name}'
        song_data['Duration'] = time.strftime('%M:%S', time.gmtime(song_data['Duration']) )
        song_query.append(song_data)
    return song_query 

def add_user(db : SQLAlchemy, username, password):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    user = User(username=username, password=password, RegistrationDate=current_time)
    db.session.add(user)
    db.session.commit()

def is_user_exist(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return user.UserID
    return False

def get_user_playlist(db : SQLAlchemy, UserID):
    playlist = Playlist.query.filter_by(UserID=UserID)
    playlist_pkg = {}
    for it in playlist:
        playlist_pkg[str(it.PlaylistID)] = it.PlaylistName
    return playlist_pkg

def add_playlist(db : SQLAlchemy, UserID, PlaylistName):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    playlist = Playlist(UserID=UserID, CreationDate=current_time, PlaylistName=PlaylistName)
    db.session.add(playlist)
    db.session.commit()

def del_playlist(db : SQLAlchemy, PlaylistID):
    songlist = SongList.query.filter_by(PlaylistID=PlaylistID)
    for it in songlist:
        db.session.delete(it)

    playlist = Playlist.query.filter_by(PlaylistID=PlaylistID).first()
    db.session.delete(playlist)
    db.session.commit()

def rename_playlist(db : SQLAlchemy, PlaylistID, PlaylistName):
    playlist = Playlist.query.filter_by(PlaylistID=PlaylistID).first()
    print(PlaylistID, playlist)
    playlist.PlaylistName = PlaylistName
    db.session.commit()

def add_song_to_playlist(db : SQLAlchemy, PlaylistID, SongID):
    songlist = SongList(PlaylistID=PlaylistID, SongID=SongID)
    db.session.add(songlist)
    db.session.commit()

def del_song_from_playlist(db : SQLAlchemy, PlaylistID, SongID):
    song = SongList.query.filter_by(PlaylistID=PlaylistID, SongID=SongID).first()
    db.session.delete(song)
    db.session.commit()