import os, sys
import json
from sqlalchemy import Column, Integer, String, create_engine, Date
from flask_sqlalchemy import SQLAlchemy
from datetime import date



DATABASE_PATH='postgresql://postgres:Habibah1234&@localhost:5432/castagency'

#DATABASE_PATH = os.environ['DATABASE_URL']

db = SQLAlchemy()

#setup_db(app) binds a flask application and a SQLAlchemy service

def setup_db(app, database_path=DATABASE_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
    

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    new_actor = (Actors(name='John', gender='Male', age=25))

    new_movie = (Movies(title = 'To the rescue', release_date = date.today()))
    print(new_movie.id, "Hell", new_actor)
    #sys.exit()

    
    new_actor.insert()
    new_movie.insert()
    new_performance = Performance.insert().values(Movie_id = new_movie.id, Actor_id = new_actor.id, actor_fee = 500.00 )
    db.session.execute(new_performance) 
    db.session.commit()

Performance = db.Table('Performance',db.Model.metadata,
    db.Column('Movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('Actor_id', db.Integer, db.ForeignKey('actors.id')),
    db.Column('actor_fee', db.Float)
)

#Actors Table & Model

class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name' : self.name,
            'gender': self.gender,
            'age': self.age
            }

#Movies Table & Model

class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    actors = db.relationship('Actors', secondary=Performance, backref=db.backref('performances', lazy='joined'))


    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title' : self.title,
            'release_date': self.release_date
            }