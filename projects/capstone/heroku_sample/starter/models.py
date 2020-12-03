import os

from sqlalchemy import Column, String, create_engine, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_path = os.environ.get('DATABASE_URL')
if not database_path:
  database_name = "capstonetest"
  database_path = "postgres://{}:{}@{}/{}".format('rhee','projectpassword','localhost:5432', database_name)

'''
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgres://dxnedpuqpodrjx:\
      20e19711adfec6fd041f706ba86cfd4b4e31380bf410fafc9cecbfdef5e06523@ec2-34-239-241-25\
        .compute-1.amazonaws.com:5432/d45n8hen0ih0e2'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
'''

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    #app.config.from_object('config')

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #migrate = Migrate(app, db)
    db.create_all()

'''
Movie
Have title and release year
'''
class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(String)
  cast = relationship('Cast', backref='Movie')

  def __init__(self, title, release_date=""):
    self.title = title
    self.release_date = release_date

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date
      }

  '''
  insert()
      inserts a new movie into a database
      the movie must have a unique name
      the movie must have a unique id or null id
      EXAMPLE
          movie = Movie(title=req_title, release_date=req_release_date)
          movie.insert()
  '''
  def insert(self):
      db.session.add(self)
      db.session.commit()

  '''
  delete()
      deletes a movie from a database
      the movie must exist in the database
      EXAMPLE
        movie = Movie(title=req_title, release_date=req_release_date)
        movie.delete()
  '''
  def delete(self):
      db.session.delete(self)
      db.session.commit()

  '''
  update()
      updates a movie in a database
      the movie must exist in the database
      EXAMPLE
          movie = Movie.query.filter(Movie.id == id).one_or_none()
          movie.title = 'Parasite'
          movie.update()
  '''
  def update(self):
      db.session.commit()

  '''
  def __repr__(self):
      return json.dumps(self.short())
  '''

class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)
  cast = db.relationship('Cast', backref='Actor')

  def __init__(self, name, age, gender=""):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
      }

  '''
  insert()
      inserts a new actor into a database
      the actor must have a unique name
      the actor must have a unique id or null id
      EXAMPLE
        actor = Actor(name=req_name, age=req_age, gender=req_gender)
        actor.insert()
  '''
  def insert(self):
      db.session.add(self)
      db.session.commit()

  '''
  delete()
      deletes a actor from a database
      the actor must exist in the database
      EXAMPLE
        actor = Actor(name=req_name, age=req_age, gender=req_gender)
        actor.delete()
  '''
  def delete(self):
      db.session.delete(self)
      db.session.commit()

  '''
  update()
      updates a actor in a database
      the actor must exist in the database
      EXAMPLE
          actor = Actor.query.filter(Actor.id == id).one_or_none()
          actor.name = 'Song Kang-ho'
          actor.update()
  '''
  def update(self):
      db.session.commit()


class Cast(db.Model):
  __tablename__ = 'cast_list'
    
  id = Column(Integer, primary_key=True)
  #movie_id = Column(Integer)
  #actor_id = Column(Integer)
  movie_id = Column(Integer, ForeignKey(Movie.id))
  actor_id = Column(Integer, ForeignKey(Actor.id))
  role = Column(String)

  def __init__(self, movie_id, actor_id, role=""):
    self.movie_id = movie_id
    self.actor_id = actor_id
    self.role = role

  def format(self):
    return {
      'id': self.id,
      'movie_id': self.movie_id,
      'actor_id': self.actor_id,
      'role': self.role
      }

  '''
  assign()
      assigns a new role to an actor
      EXAMPLE
        role = Cast(movie_id=req_movie_id, actor_id=req_actor_id, role=req_role)
        role.assign()
  '''
  def assign(self):
      db.session.add(self)
      db.session.commit()

  '''
  unassign()
      unassigns a role from an actor
      EXAMPLE
        role = Cast(movie_id=req_movie_id, actor_id=req_actor_id, role=req_role)
        role.unassign()
  '''
  def unassign(self):
      db.session.delete(self)
      db.session.commit()
  
  '''
  def update(self):
      db.session.commit()
  '''

