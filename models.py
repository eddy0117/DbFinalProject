from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Song(db.Model):
    __tablename__ = 'Song'
    SongID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(80), unique=False, nullable=False)
    Album = db.Column(db.String(80), unique=False, nullable=False)
    ReleaseYear = db.Column(db.Integer, unique=False, nullable=False)
    Duration = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, Title, Album, ReleaseYear, Duration):
        self.Title = Title
        self.Album = Album
        self.ReleaseYear = ReleaseYear
        self.Duration = Duration

    # def __repr__(self):
    #     return '<User %r>' % self.username
    
class User(db.Model):
    __tablename__ = 'User'
    UserID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    RegistrationDate = db.Column(db.String(120), unique=False, nullable=False)


    def __init__(self, username, password, RegistrationDate):
        self.username = username
        self.password = password
        self.RegistrationDate = RegistrationDate
    # def __repr__(self):
    #     return '<User %r>' % self.username

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # app.run(debug=True)
        # song1 = Song(Title='Song1', Album='Album1', ReleaseYear=2020, Duration=200)
        # db.session.add(song1)
        # db.session.commit()