from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from models import db, Song#, User, Playlist, 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == "__main__":
    with app.app_context():
        song2 = Song(Title='Song2', Album='Album2', ReleaseYear=2020, Duration=200)
        db.session.add(song2)
        song3 = Song(Title='Song3', Album='Album3', ReleaseYear=2020, Duration=200)
        db.session.add(song3)
        db.session.commit()