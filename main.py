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
from api.songsapi import songs_api
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
app.register_blueprint(songs_api)
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


# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port="8080")
