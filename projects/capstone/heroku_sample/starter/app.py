import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from auth import AuthError, requires_auth
from models import setup_db, Movie, Actor, Cast
import json

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_info():
        try:
            movies = Movie.query.all()
            actors = Actor.query.all()

            formatted_movies = [movie.title for movie in movies]
            formatted_actors = [actor.name for actor in actors]

            return jsonify({
                "success": True, 
                "movies": formatted_movies,
                "actors": formatted_actors
            }), 200
        
        except:
            abort(422)

    '''
    GET /actors
        it requires the 'view:actors' permission.
            - Casting Assistant, Csting Director, Executive Producer

                    it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
            where drinks is the list of drinks
            or appropriate status code indicating reason for failure   
    '''  


    @app.route('/actors')
    @requires_auth('view:actors')
    def get_actors(payload):
        try:
            actors = Actor.query.all()

            formatted_actors = [actor.format() for actor in actors]

            return jsonify({
                "success": True, 
                "actors": formatted_actors
            }), 200

        except:
            abort(422)


    @app.route('/movies')
    @requires_auth('view:movies')
    def get_movies(payload):
        try:
            movies = Movie.query.all()

            formatted_movies = [movie.format() for movie in movies]

            return jsonify({
                "success": True,
                "movies": formatted_movies
            }), 200

        except:
            abort(422)


    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):
        deleted_actor = Actor.query.filter_by(id=actor_id).one_or_none()

        # 404 error: if <id> is not found
        if deleted_actor is None:
            abort(404)
        
        formatted_actors = [deleted_actor.format()]
        deleted_actor.delete()

        return jsonify({
            "success": True,
            "delete": formatted_actors
        }), 200


    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):
        deleted_movie = Movie.query.filter_by(id=movie_id).one_or_none()
        deleted_cast = Cast.query.filter_by(movie_id=movie_id).all()

        # 404 error: if <id> is not found
        if deleted_movie is None:
            abort(404)
        
        formatted_movies = [deleted_movie.format()]
        deleted_movie.delete()

        if len(deleted_cast) > 0:
            for cast in deleted_cast:
                cast.unassign() 
        
        return jsonify({
            "success": True,
            "delete": formatted_movies
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actors')
    def add_actors(payload):
        requests = request.get_json()

        name = requests['name']
        age = requests['age']
        gender = requests['gender']

        # For checking it is newly added actor or not
        if Actor.query.filter_by(name=name).one_or_none():
            abort(422)

        new_actor = Actor(name=name, age=age, gender=gender)
        new_actor.insert()
        formatted_actors = [new_actor.format()]

        return jsonify({
            "success": True,
            "actors": formatted_actors
        }), 200


    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movies')
    def add_movies(payload):
        requests = request.get_json()

        title = requests['title']
        release_date = requests['release_date']

        # For checking it is newly added movie or not
        if Movie.query.filter_by(title=title).one_or_none():
            abort(422)

        new_movie = Movie(title=title, release_date=release_date)
        new_movie.insert()
        formatted_movies = [new_movie.format()]

        return jsonify({
            "success": True,
            "movies": formatted_movies
        }), 200


    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('modify:actors')
    def update_actors(payload, actor_id):
        updated_actor = Actor.query.filter_by(id=actor_id).one_or_none()

        if updated_actor is None:
            abort(404)

        requests = request.get_json()

        for patched_attribute in requests:
            if patched_attribute == 'name':
                updated_actor.name = requests['name']
            elif patched_attribute == 'age':
                updated_actor.age = requests['age']
            elif patched_attribute == 'gender':
                updated_actor.gender = requests['gender']

        updated_actor.update()

        formatted_actors = [updated_actor.format()]

        return jsonify({
            "success": True,
            "actors": formatted_actors
        }), 200


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('modify:movies')
    def update_movies(payload, movie_id):   
        updated_movie = Movie.query.filter_by(id=movie_id).one_or_none()

        if updated_movie is None:
            abort(404)

        requests = request.get_json()

        for patched_attribute in requests:
            if patched_attribute == 'title':
                updated_movie.title = requests['title']
            elif patched_attribute == 'release_date':
                updated_movie.release_date = requests['release_date']

        updated_movie.update()

        formatted_movies = [updated_movie.format()]

        return jsonify({
            "success": True,
            "movies": formatted_movies
        }), 200


    @app.route('/cast')
    @requires_auth('view:cast')
    def view_cast(payload):
        try:
            cast_list = Cast.query.all()
            
            formatted_cast = [cast.format() for cast in cast_list]

            return jsonify({
                "success": True,
                "cast": formatted_cast
            }), 200
        
        except:
            abort(422)


    @app.route('/cast', methods=['POST'])
    @requires_auth('add:cast')
    def add_cast(payload):
        requests = request.get_json()
        
        movie_id = requests['movie_id']
        actor_id = requests['actor_id']

        role = requests['role']

        casted_movie = Movie.query.filter_by(id=movie_id).one_or_none()
        casted_actor = Actor.query.filter_by(id=actor_id).one_or_none()

        if casted_movie is None:
            abort(404)

        if casted_actor is None:
            abort(404)

        new_cast = Cast(movie_id=movie_id, actor_id=actor_id, role=role)
        new_cast.assign()
        formatted_cast = [new_cast.format()]

        return jsonify({
            "success": True,
            "cast": formatted_cast
        })
        

    @app.route('/cast/<int:cast_id>', methods=['DELETE'])
    @requires_auth('delete:cast')
    def delete_cast(payload, cast_id):       
        deleted_cast = Cast.query.filter_by(id=cast_id).one_or_none()

        if deleted_cast is None:
            abort(404)
        
        formatted_cast = [deleted_cast.format()]
        deleted_cast.unassign()
        
        return jsonify({
            "success": True,
            "cast": formatted_cast
        })

        '''
        try:
            deleted_cast = Cast.query.filter_by(id=cast_id).one_or_none()

            if deleted_cast is None:
                abort(404)
            
            formatted_cast = [deleted_cast.format()]
            deleted_cast.unassign()
            
            return jsonify({
                "success": True,
                "cast": formatted_cast
            })
        
        except:
            abort(422)
        '''
    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code
   
    return app

app = create_app()

'''
def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()
'''


if __name__ == '__main__':
    app.run()

'''
if __name__ == '__main__':
    port = init(os.environ.get("PORT", 5432))
    app.run(host='127.0.0.1', port=port)
'''

