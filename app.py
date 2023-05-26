import os
import pandas as pd
from flask import render_template, Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Specify the path to the SQLite database
db_path = os.path.join(os.getcwd(), 'instance', 'volumes', 'song_data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# Initialize SQLAlchemy with this Flask app
db = SQLAlchemy(app)

# Define your model schema here
class MySongs(db.Model):
    # Define your model schema here
    # Make sure to include the necessary columns that match your CSV file
    __tablename__ = 'songs'  # Specify the name of your table

    id = db.Column(db.Integer, primary_key=True)  # Example column: an integer primary key
    title = db.Column(db.String(255))  # Example column: a string column with length 255
    artist = db.Column(db.String(255))
    top_genre = db.Column(db.String(255))
    year = db.Column(db.Integer)
    bpm = db.Column(db.Integer)
    energy = db.Column(db.Integer)
    danceability = db.Column(db.Integer)
    loudness = db.Column(db.Integer)
    liveness = db.Column(db.Integer)
    valence = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    acousticness = db.Column(db.Integer)
    speechiness = db.Column(db.Integer)
    popularity = db.Column(db.Integer) # Example column: an integer column

    # Additional columns can be defined here

    def __init__(self, title, artist, top_genre, year, bpm, energy, danceability, loudness, liveness, valence, duration, acousticness, speechiness, popularity):
        self.title = title
        self.artist = artist
        self.top_genre = top_genre
        self.year = year 
        self.bpm = bpm 
        self.energy = energy 
        self.danceability = danceability
        self.loudness = loudness 
        self.liveness = liveness 
        self.valence = valence 
        self.duration = duration 
        self.acousticness = acousticness
        self.speechiness = speechiness
        self.popularity = popularity

from flask import jsonify

@app.route('/songdatabase')
def songdatabase():
    # Fetch data from the songs table into a DataFrame
    df = pd.read_sql_table('songs', db.engine)

    # Convert the DataFrame into a list of dictionaries
    data = df.to_dict(orient='records')

    # Return a JSON response
    return jsonify(data)


# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port="8080")
