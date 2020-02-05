from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth

def create_app(test_config=None):

  ## App Setup

  app = Flask(__name__)
  CORS(app)
  setup_db(app)

  ## API Routes

  @app.route('/')
  def welcome():
    return 'Welcome to the MovieCast API'

  @app.route('/actors')
  @requires_auth('view:actors')
  def view_actors(payload):
    try:
      actors = [actor.format for actor in Actor.query.all()]

      return jsonify({
          'success': True,
          'actors': actors
      }), 200
    except:
      abort(422)

  @app.route('/movies')
  @requires_auth('view:movies')
  def view_movies(payload):
    try:
      movies = [movie.format for movie in Movie.query.all()]

      return jsonify({
          'success': True,
          'movies': movies
      }), 200
    except:
      abort(422)

  @app.route('/actors', methods=['POST'])
  @requires_auth('add:actor')
  def create_actor(payload):
      body = request.get_json()

      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)

      if name is None or age is None or gender is None:
          abort(400)

      try:
          actor = Actor(name=name, age=age, gender=gender)
          actor.insert()

          created_actor = Actor.query.filter_by(name=name).one_or_none()

          return jsonify({
              'success': True,
              'actors': [created_actor.format]
          }), 201

      except:
          abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('add:movie')
  def create_movie(payload):
      body = request.get_json()

      title = body.get('title', None)
      release_date = body.get('release_date', None)

      if title is None or release_date is None:
          abort(400)

      try:
          movie = Movie(title=title, release_date=release_date)
          movie.insert()

          created_movie = Movie.query.filter_by(title=title).one_or_none()

          return jsonify({
              'success': True,
              'movies': [created_movie.format]
          }), 201

      except:
          abort(422)

  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('modify:actor')
  def update_actors(payload, id):
    error = None

    try:
      body = request.get_json()

      actor = Actor.query.filter_by(id=id).one_or_none()
      
      if actor is None:
        error = 404
        abort(404)
      
      if not body:
        error = 400
        abort(400)

      actor.name = body.get('name', actor.name)
      actor.age = body.get('age', actor.age)
      actor.gender = body.get('gender', actor.gender)
      actor.update()

      return jsonify({
          'success': True,
          'actors': [actor.format]
      }), 200

    except:
      if error == 404:
        abort(404)
      if error == 400:
        abort(400)
      abort(422)

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('modify:movie')
  def update_movies(payload, id):
    error = None

    try:
      body = request.get_json()

      movie = Movie.query.filter_by(id=id).one_or_none()
      
      if movie is None:
        error = 404
        abort(404)
      
      if not body:
        error = 400
        abort(400)

      movie.title = body.get('title', movie.title)
      movie.release_date = body.get('release_date', movie.release_date)
      movie.update()

      return jsonify({
          'success': True,
          'actors': [movie.format]
      }), 200

    except:
      if error == 404:
        abort(404)
      if error == 400:
        abort(400)
      abort(422)

  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actors(payload, id):
      try:
        actor = Actor.query.filter_by(id=id).one_or_none()
        
        if actor is None:
          abort(404)

        actor.delete()

        return jsonify({
          'success': True,
          'deleted_id': actor.id
        }), 200

      except:
        abort(422)

  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movies(payload, id):
    try:
      movie = Movie.query.filter_by(id=id).one_or_none()
      
      if movie is None:
        abort(404)

      movie.delete()

      return jsonify({
        'success': True,
        'deleted_id': movie.id
      }), 200

    except:
      abort(422)

  ## Error Handling

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "not found"
    }), 404

  @app.errorhandler(405)
  def moethod_not_allowed(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
    }), 422

  @app.errorhandler(AuthError)
  def auth_error(e):
    return jsonify({
      'success':False,
      'status': e.status_code,
      'message': e.error['description']
    }), e.status_code

  return app

app = create_app()

if __name__ == '__main__':
  app.run()
