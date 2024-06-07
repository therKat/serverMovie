import sqlite3

DATABASE = 'movie.sqlite'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_movie(movie_id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movie WHERE id = ?', (movie_id,)).fetchone()
    conn.close()
    return movie

def get_all_movies():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movie').fetchall()
    conn.close()
    return movies

def create_movie(title, year, description, director, poster, trailer):
    conn = get_db_connection()
    conn.execute('INSERT INTO movie (title, year, description, director, poster, trailer) VALUES (?, ?, ?, ?, ?, ?)',
                 (title, year, description, director, poster, trailer))
    conn.commit()
    conn.close()

def update_movie(movie_id, title, year, description, director, poster, trailer):
    conn = get_db_connection()
    conn.execute('UPDATE movie SET title = ?, year = ?, description = ?, director = ?, poster = ?, trailer = ? WHERE id = ?',
                 (title, year, description, director, poster, trailer, movie_id))
    conn.commit()
    conn.close()

def delete_movie(movie_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM movie WHERE id = ?', (movie_id,))
    conn.commit()
    conn.close()
