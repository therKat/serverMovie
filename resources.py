from flask import request, jsonify
from flask_restful import Resource
from models import get_movie, get_all_movies, create_movie, update_movie, delete_movie, allowed_file
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'

class MovieResource(Resource):
    def get(self, movie_id=None):
        if movie_id:
            movie = get_movie(movie_id)
            if movie is None:
                return {'error': 'Movie not found'}, 404
            return dict(movie), 200
        else:
            movies = get_all_movies()
            return [dict(movie) for movie in movies], 200

    def post(self):
        data = request.form
        image_file = request.files.get('poster')
        video_file = request.files.get('trailer')

        # Kiểm tra định dạng file
        if image_file and allowed_file(image_file.filename) and video_file and allowed_file(video_file.filename):
            title = data['title']
            year = data['year']
            description = data['description']
            director = data['director']

            # Lưu file ảnh
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image_file.save(image_path)

            # Lưu file video
            video_filename = secure_filename(video_file.filename)
            video_path = os.path.join(UPLOAD_FOLDER, video_filename)
            video_file.save(video_path)

            # Lưu thông tin phim vào cơ sở dữ liệu
            create_movie(title, year, description, director, image_path, video_path)
            return {'message': 'Movie created successfully'}, 201
        else:
            return {'error': 'Invalid file format'}, 400
    def put(self, movie_id):
        data = request.get_json()
        movie = get_movie(movie_id)
        if movie is None:
            return {'error': 'Movie not found'}, 404
        update_movie(movie_id, data['title'], data['year'], data['description'], data['director'], data.get('poster'), data.get('trailer'))
        return {'message': 'Movie updated successfully'}, 200

    def delete(self, movie_id):
        movie = get_movie(movie_id)
        if movie is None:
            return {'error': 'Movie not found'}, 404
        delete_movie(movie_id)
        return {'message': 'Movie deleted successfully'}, 204
