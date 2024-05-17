from models import db,  Song, User, Playlist, Artist, SongList
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import time
# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

def get_songs_data(songlist):
    song_query = []
    if isinstance(songlist[0], Song):
        for s in songlist:
            song = Song.query.filter_by(SongID=s.SongID).first()
            song_data = to_dict(song)
            artist = Artist.query.filter_by(SongID=s.SongID)
            song_data['Artist'] = artist[0].Name
            for art in artist[1:]:
                song_data['Artist'] += f', {art.Name}'
            song_data['Duration'] = time.strftime('%M:%S', time.gmtime(song_data['Duration']) )
            song_query.append(song_data)
        return song_query
    else:
        for s in songlist:
            song = Song.query.filter_by(SongID=s[0].SongID).first()
            song_data = to_dict(song)
            artist = Artist.query.filter_by(SongID=s[0].SongID)
            song_data['Artist'] = artist[0].Name
            for art in artist[1:]:
                song_data['Artist'] += f', {art.Name}'
            song_data['Duration'] = time.strftime('%M:%S', time.gmtime(song_data['Duration']) )
            song_query.append(song_data)
        return song_query

def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def add_song(db : SQLAlchemy, Title, Album, ReleaseYear, Duration, PictureSrc, SongSrc, *ArtistName):
    song = Song(Title=Title, Album=Album, ReleaseYear=ReleaseYear, Duration=Duration, PictureSrc=PictureSrc, SongSrc=SongSrc)
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

def search_song(db : SQLAlchemy, kw):
   
    song_exist_list = []
    song_query = []
 
    S_join_A = db.session.query(Song, Artist).join(Artist, Artist.SongID == Song.SongID)
    search_query = S_join_A.filter(db.or_(Song.Album.ilike(f'%{kw}%'), Song.Title.ilike(f'%{kw}%'), Artist.Name.ilike(f'%{kw}%'))).all()
    for it in search_query:
        if it[0].SongID not in song_exist_list:
            song_exist_list.append(it[0].SongID)
        else:
            continue
        song_data = {**to_dict(it[0]), **to_dict(it[1])}
        song_data['Duration'] = time.strftime('%M:%S', time.gmtime(song_data['Duration']) )
        song_query.append(song_data)
    return song_query

def get_topN_famous_song(n):
    songs = Song.query.order_by((Song.PFemale + Song.PMale).desc()).limit(n).all()
    return get_songs_data(songs)

def get_topN_famous_album(n):
    songs = []
    albums = db.session.query(Song.Album, db.func.sum(Song.PFemale + Song.PMale)).group_by(Song.Album).order_by(db.func.sum(Song.PFemale + Song.PMale).desc()).limit(n)
    for it in albums:
        # it[0] is Album name, it[1] is Pcount
        song_list = Song.query.filter(Song.Album == it[0]).all()
        songs.append(get_songs_data(song_list))
        
    return songs, [it[1] for it in albums]

def get_topN_famous_artist(n):
    songs = []
    S_join_A = db.session.query(Song, Artist).join(Artist, Artist.SongID == Song.SongID)
    artists = db.session.query(Artist.Name, db.func.sum(Song.PFemale + Song.PMale)).join(Artist, Artist.SongID == Song.SongID).group_by(Artist.Name).order_by(db.func.sum(Song.PFemale + Song.PMale).desc()).limit(n).all()
    for artist in artists:
        # artist[0] is Artist name, artist[1] is Pcount
        songlist = S_join_A.filter(Artist.Name == artist[0]).all()
        songs.append(get_songs_data(songlist))
    
    return songs, [it[1] for it in artists]

def add_user(db : SQLAlchemy, username, password, Gender):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    user = User(username=username, password=password, RegistrationDate=current_time, Gender=Gender)
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
        songlist = SongList.query.filter_by(PlaylistID=it.PlaylistID).all()
        song_query = get_songs_data(songlist)
        playlist_pkg[str(it.PlaylistID)] = [it.PlaylistName, f"{it.CreationDate.split('-')[0]}年{it.CreationDate.split('-')[1]}月{it.CreationDate.split('-')[2].split(' ')[0]}日", song_query]
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