from flask import Flask, request, jsonify
from datetime import datetime
from models import db, Movie
from config import Config
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/initdb')
def initdb():
    db.create_all()
    return "Database tables created!", 200

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.to_dict() for movie in movies]), 200

@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        return jsonify(movie.to_dict()), 200
    return jsonify({"error": "Movie not found"}), 404

@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    try:
        new_movie = Movie(
            title=data['title'],
            description=data.get('description'),
            rating=float(data['rating']),
            release_date=datetime.strptime(data['release_date'], '%Y-%m-%d').date()
        )
        db.session.add(new_movie)
        db.session.commit()
        return jsonify(new_movie.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    data = request.get_json()
    try:
        movie.title = data.get('title', movie.title)
        movie.description = data.get('description', movie.description)
        movie.rating = float(data.get('rating', movie.rating))
        if 'release_date' in data:
            movie.release_date = datetime.strptime(data['release_date'], '%Y-%m-%d').date()
        db.session.commit()
        return jsonify(movie.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
