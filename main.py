import threading

# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries

# import "packages" from "this" project
from __init__ import app, db  # Definitions initialization
from model.jokes import initJokes
from model.users import initUsers
from model.players import initPlayers
# from model.song_data import db
from flask import Flask

# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.joke import joke_api # Blueprint import api definition
from api.user import user_api # Blueprint import api definition
from api.player import player_api
# from api.song_data import songs_api


# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition

# import os
# from flask_sqlalchemy import SQLAlchemy

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///song_data.db'
# db = SQLAlchemy(app)

# Rest of your code...


# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# register URIs
app.register_blueprint(joke_api) # register api routes
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects) # register app pages

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/stub/')  # connects /stub/ URL to stub() function
def stub():
    return render_template("stub.html")

@app.before_first_request
def activate_job():  # activate these items 
    initJokes()
    initUsers()
    initPlayers()


import os
import pandas as pd
from flask import render_template

@app.route('/songdata')
def songdata():
    # Path to the CSV file
    csv_path = os.path.join(app.static_folder, 'songdata.csv')

    # Read the CSV file into a pandas dataframe
    df = pd.read_csv(csv_path)

    # Render the dataframe as an HTML table using Jinja2
    return render_template('songdata.html', table=df.to_html(index=False))

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

from flask import request
import json
from flask import Blueprint, request, jsonify
#from flask_restful import Api, Resource # used for REST API building


def write_sql_table(table_name):
    from flask import request
    # Retrieve the data from the request
    body = request.get_json()
    title = body.get('title')
    artist = body.get('artist')
    top_genre = body.get('top_genre')
    year = body.get('year')
    bpm = body.get('bpm')
    energy = body.get('energy')
    danceability = body.get('danceability')
    loudness = body.get('loudness')
    liveness = body.get('liveness')
    valence = body.get('valence')
    duration = body.get('duration')
    acousticness = body.get('acousticness')
    speechiness = body.get('speechiness')
    popularity = body.get('popularity')

    # Check for null values
    if None in (title, artist, top_genre, year, bpm, energy, danceability, loudness, liveness, valence, duration, acousticness, speechiness, popularity):
        return jsonify({'message': 'Cannot insert row with null values'})

    # Construct the SQL insert statement
    insert_statement = f"INSERT INTO {table_name} (title, artist, top_genre, year, bpm, energy, " \
                       f"danceability, loudness, liveness, valence, duration, acousticness, speechiness, popularity) " \
                       f"VALUES (:title, :artist, :top_genre, :year, :bpm, :energy, :danceability, " \
                       f":loudness, :liveness, :valence, :duration, :acousticness, :speechiness, :popularity)"

    # Execute the insert statement with the provided data
    db.session.execute(
        insert_statement,
        {
            'title': title,
            'artist': artist,
            'top_genre': top_genre,
            'year': year,
            'bpm': bpm,
            'energy': energy,
            'danceability': danceability,
            'loudness': loudness,
            'liveness': liveness,
            'valence': valence,
            'duration': duration,
            'acousticness': acousticness,
            'speechiness': speechiness,
            'popularity': popularity
        }
    )

    # Commit the changes to the database
    db.session.commit()

# delete function is below
def delete_sql_table(table_name, title):
    # Construct the SQL delete statement
    delete_statement = f"DELETE FROM {table_name} " \
                       f"WHERE title = :title"

    # Execute the delete statement with the provided data
    db.session.execute(delete_statement, {'title': title})

    # Commit the changes to the database
    db.session.commit()

# Usage example:
@app.route('/create', methods=['POST'])
def create():
    write_sql_table('songs')

@app.route('/delete', methods=['DELETE'])
def delete():
    # Check if the request contains JSON data
    if request.is_json:
        body = request.get_json()
        title = body.get('title')
        delete_sql_table('songs', title)
    else:
        return jsonify({'error': 'Invalid JSON data'})

# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port="8080")
