import sp
from flask import Flask, request, url_for, session, redirect, render_template

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Defining consts
CLIENT_ID = "2d16731d8d8a49b18162db75c7b5f07f"
CLIENT_SECRET = "816f28070acd403fbcf5182b702afc0c"
TOKEN_INFO = "token info"
SECRET_KEY = "asdf"

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for("redirectPage", _external=True),
        scope="user-top-read user-library-read"
    )

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def hello_world():
    from os import name
    return render_template('index.html', title='Welcome', username=name)

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/redirectPage")
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("receipt", _external=True))


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    return token_info

@app.route('/receipt')
def receipt():
    user_token = get_token()
    sp = spotipy.Spotify(auth=user_token['access_token']
    )

   short_term = sp.current_user_top_tracks(
        limit=10,
        offset=0,
        time_range="short term",
    )
medium_term = sp.current_user_top_tracks(
        limit=10,
        offset=0,
        time_range="medium term",
    )
long_term = sp.curent_user_top_tracks(
        limit=10,
        offset=0,
        time_range="long term",
    )
return render_template('receipt.html', short_term=short_term, medium_term=medium_term, long_term=long_term, currentTime=gmtime())
