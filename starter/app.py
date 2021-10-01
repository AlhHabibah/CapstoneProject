import os
import _json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Actors, Movies, Performance
from auth import AuthError, requires_auth


RECS_PER_PAGE = 12

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    db_drop_and_create_all()
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers','GET, POST, PATCH, DELETE, OPTIONS')
        return response
################################################################
    
    
    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * RECS_PER_PAGE
        end = start + RECS_PER_PAGE

        recs_format = [dRecord.format() for dRecord in selection]
        return recs_format[start:end]
    ################################################

    @app.route('/actors', methods=['GET'])                                    #this method is used to retrieve all actors
    @requires_auth(permission='get:actors')
    def get_actors(payload):
        try:
            selections = Actors.query.order_by(Actors.id).all()
            pagedActors = paginate_questions(request, selections)
            totalActors = len(selections)
            return jsonify({
                'success': True,
                'actors': pagedActors,
                'total-actors': totalActors
            })
        except Exception:
            abort(422)

    ###################################################

    @app.route('/actors', methods=['POST'])             #this method is used to add a new actor
    @requires_auth(permission='post:actors')
    def post_actors(payload):
        addActor = request.get_json()
        actorName = addActor.get('name')
        actorGender = addActor.get('gender')
        actorAge = addActor.get('age')
        if actorName is None:
            abort(422)
        if actorGender is None:
            abort(422)
        if actorAge is None:
            abort(422)
        try:
            newActor = Actors(name=actorName,gender=actorGender,age=actorAge)
            newActor.insert()
            return jsonify({
                "success": True,
                "actor-added": newActor.id
            })
        except Exception:
            abort(422)

    ##########################################################

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def patch_actors(payload, id):
        actor = Actors.query.filter(Actors.id == id).first()
        if not actor:
            abort(404)
        updateActorReq = request.get_json()
        if updateActorReq is None:
            abort(422)
        try:
            if 'name' in updateActorReq:
                actor.name = updateActorReq['name']
            if 'gender' in updateActorReq:
                actor.gender = updateActorReq['gender']
            if 'age' in updateActorReq:
                actor.age = updateActorReq['age']
            actor.update()
            return jsonify({
                "success": True,
                "actor-updated": actor.id
            })
        except Exception:
            abort(422)

    ####################################################

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')                                  #to delete selected actor based on id
    def delete_actors(payload, id):
        actor = Actors.query.filter(Actors.id == id).first()
        if not actor:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                "success": True,
                "actor-deleted": actor.id })
        except Exception:
            abort(422)

    ##########################################################

    @app.route('/movies', methods=['GET'])                                    #to retrieve all movies
    @requires_auth(permission='get:movies')
    def get_movies(payload):
        try:
            selections = Movies.query.order_by(Movies.id).all()
            pagedMovies = paginate_questions(request, selections)
            totalMovies = len(selections)
            return jsonify({
                'success': True,
                'movies': pagedMovies,
                'total-movies': totalMovies  })
        except Exception:
            abort(422)

    ###################################################
    @app.route('/movies', methods=['POST'])                              #to add new movie
    @requires_auth(permission='post:movies')
    def post_movies(payload):
        addMovie = request.get_json()
        movieTitle = addMovie.get('title')
        movieRls_date = addMovie.get('release_date')

        if movieTitle is None:
            abort(422)
        if movieRls_date is None:
            abort(422)
        try:
            newMovie = Movies(title=movieTitle, release_date=movieRls_date)
            newMovie.insert()
            return jsonify({
                "success": True,
                "movie-added": new_movie.id })
        except Exception:
            abort(422)

    #################################################

    @app.route('/movies/<int:id>', methods=['PATCH'])      
    @requires_auth(permission='patch:movies')
    def patch_movies(payload, id):
        movie = Movies.query.filter(Movies.id == id).first()
        if not movie:
            abort(404)
        updateMovieReq = request.get_json()

        if updateMovieReq is None:
            abort(422)

        try:
            if 'title' in updateMovieReq:
                movie.title = updateMovieReq['title']

            if 'release_date' in updateMovieReq:
                movie.release_date = updateMovieReq['release_date']

            movie.update()

            return jsonify({
                "success": True,
                "movie-updated": movie.id
            })

        except Exception:
            abort(422)
###############################################

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movies(payload, id):
        movie = Movies.query.filter(Movies.id == id).first()

        if not movie:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                "success": True,
                "movie-deleted": movie.id
            })

        except Exception:
            abort(422)

 
   # Error handlers for possible errors including 400, 401, 403,404, 405,422,500
    @app.errorhandler(400)
    def badRequest(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def accessForbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden/Access Denied"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def notAllowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocess entity"
        }), 422

    @app.errorhandler(500)
    def serverError(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error
        }), e.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
