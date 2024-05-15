from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Song(db.Model):
    __tablename__ = 'song'
    SongID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(80), unique=False, nullable=False)
    Album = db.Column(db.String(80), unique=False, nullable=False)
    ReleaseYear = db.Column(db.Integer, unique=False, nullable=False)
    Duration = db.Column(db.Integer, unique=False, nullable=False)
    PictureSrc = db.Column(db.String(80), unique=False, nullable=True)
    SongSrc = db.Column(db.String(80), unique=True, nullable=True)
    PMale = db.Column(db.Integer, unique=False, nullable=True)
    PFemale = db.Column(db.Integer, unique=False, nullable=True)
    # SongList = db.relationship('SongList', backref='song')

    def __init__(self, Title, Album, ReleaseYear, Duration, PictureSrc, SongSrc):
        self.Title = Title
        self.Album = Album
        self.ReleaseYear = ReleaseYear
        self.Duration = Duration
        self.PictureSrc = PictureSrc
        self.SongSrc = SongSrc
        self.PMale = 0
        self.PFemale = 0

class Artist(db.Model):
    __tablename__ = 'artist'
    SongID = db.Column(db.Integer, db.ForeignKey('song.SongID'), primary_key=True)
    Name = db.Column(db.String(80), primary_key=True)

    # Song = db.relationship('Song', backref='artist')

    def __init__(self, SongID, Name):
        self.Name = Name
        self.SongID = SongID
    
class User(db.Model):
    __tablename__ = 'user'
    UserID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    RegistrationDate = db.Column(db.String(120), unique=False, nullable=False)
    Gender = db.Column(db.String(10), unique=False, nullable=True)

    # Playlist = db.relationship('Playlist', backref='user')

    def __init__(self, username, password, RegistrationDate, Gender):
        self.username = username
        self.password = password
        self.RegistrationDate = RegistrationDate
        self.Gender = Gender

class Playlist(db.Model):
    __tablename__ = 'playlist'
    PlaylistID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    PlaylistName = db.Column(db.String(80), unique=False, nullable=False)
    CreationDate = db.Column(db.String(20), unique=False, nullable=False)

    # SongList  = db.relationship('SongList', backref='playlist')
    # User = db.relationship('User', backref='playlist')

    def __init__(self, UserID, CreationDate, PlaylistName):
        self.UserID = UserID
        self.CreationDate = CreationDate
        self.PlaylistName = PlaylistName

class SongList(db.Model):
    __tablename__ = 'songlist'
    PlaylistID = db.Column(db.Integer, db.ForeignKey('playlist.PlaylistID'), primary_key=True)
    SongID = db.Column(db.Integer, db.ForeignKey('song.SongID'), primary_key=True)

    # Playlist = db.relationship('Playlist', backref='songlist')
    # Song = db.relationship('Song', backref='songlist')

    def __init__(self, PlaylistID, SongID):
        self.PlaylistID = PlaylistID
        self.SongID = SongID

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # app.run(debug=True)
        # song1 = Song(Title='Song1', Album='Album1', ReleaseYear=2020, Duration=200)
        # db.session.add(song1)
        # db.session.commit()