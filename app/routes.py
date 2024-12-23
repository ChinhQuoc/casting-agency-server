from app import app
from flask import request, jsonify, abort, session, redirect
from .models import Movie, Actor
from auth.auth import requires_auth, AuthError
from .settings import AUTH0_DOMAIN, CLIENT_ID, LOGOUT_REDIRECT_URI, BLACKLISTED_TOKENS

# GET /actors and /movies
@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    movies = Movie.query.all()
    print(movies)
    list_movie = [movie.get_data() for movie in movies]

    return jsonify({
        'success': True,
        'movies': list_movie
    })

@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    actors = Actor.query.all()
    list_actor = [actor.get_data() for actor in actors]

    return jsonify({
        'success': True,
        'actors': list_actor
    })

@app.route('/movies/<int:id>', methods=['GET'])
@requires_auth('get:movie')
def get_movie_by_id(payload, id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    if movie is None:
        abort(404)

    movie_data = movie.get_data()
    movie_data['actors'] = [actor.get_data() for actor in movie.actors]

    return jsonify({
        'success': True,
        'movie': movie_data
    })

@app.route('/actors/<int:id>', methods=['GET'])
@requires_auth('get:actor')
def get_actor_by_id(payload, id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()

    if actor is None:
        abort(404)

    actor_data = actor.get_data()
    actor_data['movies'] = [movie.get_data() for movie in actor.movies]

    return jsonify({
        'success': True,
        'actor': actor_data
    })


# DELETE /actors/ and /movies/
@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movies(payload, id):
    movie = Movie.query.filter_by(id=id).one_or_none()

    if movie is None:
        abort(404)
    
    try:
        movie.delete()
    except:
        movie.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'delete': id
    })

@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actors(payload, id):
    actor = Actor.query.filter_by(id=id).one_or_none()

    if actor is None:
        abort(404)
    
    try:
        actor.delete()
    except:
        actor.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'delete': id
    })

# POST /actors and /movies
@app.route('/movies', methods=['POST'])
@requires_auth('post:movie')
def create_movie(payload):
    body = request.get_json()

    new_title = body.get('title', None)
    new_release_date = body.get('releaseDate', None)
    actor_ids = body.get('idsActor', [])

    try:
        if not new_title or not new_release_date:
            abort(400, description="Title and release date are required")

        actors = Actor.query.filter(Actor.id.in_(actor_ids)).all()

        movie = Movie(title=new_title, release_date=new_release_date)
        movie.actors = actors
        movie.insert()
    except:
        movie.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'movie': movie.get_data()
    })

@app.route('/actors', methods=['POST'])
@requires_auth('post:actor')
def create_actor(payload):
    body = request.get_json()

    new_name = body.get('name', None)
    new_age = body.get('age', 0)
    new_gender = body.get('gender', 'male')
    movie_ids = body.get('idsMovie', [])

    try:
        if not new_name:
            abort(400, description="Name is required")

        movies = Movie.query.filter(Movie.id.in_(movie_ids)).all()

        actor = Actor(name=new_name, age=new_age, gender=new_gender)
        actor.movies = movies
        actor.insert()
    except:
        actor.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'actor': actor.get_data()
    })

# PATCH /actors/ and /movies/
@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actor')
def update_actor(payload, id):
    actor = Actor.query.filter_by(id=id).one_or_none()

    if actor is None:
        abort(404)

    body = request.get_json()
    actor.name = body['name']
    actor.age = body['age']
    actor.gender = body['gender']
    movie_ids = body.get('idsMovie', [])

    try:
        movies = Movie.query.filter(Movie.id.in_(movie_ids)).all()
        actor.movies = movies
        actor.update()
    except:
        actor.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'actor': actor.get_data()
    })

@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movie')
def update_movie(payload, id):
    movie = Movie.query.filter_by(id=id).one_or_none()

    if movie is None:
        abort(404)

    body = request.get_json()
    movie.title = body['title']
    movie.release_date = body['releaseDate']
    actor_ids = body.get('idsActor', [])

    try:
        actors = Actor.query.filter(Actor.id.in_(actor_ids)).all()
        movie.actors = actors
        movie.update()
    except:
        movie.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'movie': movie.get_data()
    })

@app.route("/logout", methods=['POST'])
def logout():
    # Clear the user's session
    session.clear()

    # Redirect to Auth0 logout endpoint
    return jsonify({
        'success': True,
        'logout': True
    }), 200

@app.route("/revoke", methods=['POST'])
def revoke_token():
    token = request.headers.get("Authorization").split(" ")[1]
    BLACKLISTED_TOKENS.add(token)
    return jsonify({"message": "Token has been revoked."}), 200

# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": error.description if error else "unprocessable"
    }), 422

@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description if error else "Bad Request"
    }), 400

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description if error else "Resource Not Found"
    }), 404

class NotFound:
    def __init__(self, err):
        object_error = {
            self.success: False,
            self.error: 404,
            self.message: err.description if err.description else 'Resource not found!'
        }
        return (
            jsonify(object_error), 404
        )

@app.errorhandler(AuthError)
def handle_auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['message']
    }), error.status_code