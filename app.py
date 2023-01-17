from lib2to3.pgen2.pgen import DFAState
from flask import Flask, flash, request, redirect, render_template, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import pandas as pd
from flask_session import Session

#from spotify developer
CLIENT_ID="57b04b1761114d7d8343c6b5e37330f9"
CLIENT_SECRET="fe65c3db369a42538e8694d9698d0c47"
TOKEN_INFO = "token_info"

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = "qwerty123"
app.config['SESSION_COOKIE_NAME'] = 'my cookie'

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-top-read")

#if the access token is expired, get_token will get us a new one
#check if there's token data already, and if there's not, then redirect to login page
def get_token():
    #get token info, if value doesn't exist, return none
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def pop_count(top_tracks):
    pop = 0
    counter = 0
    for track in top_tracks['items']:
        popularity = track['popularity']
        pop += int(popularity)
        counter += 1
    pop = pop / counter
    return pop

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    authorize_url = sp_oauth.get_authorize_url()
    return redirect(authorize_url)

# redirects you to the index page, after authorising
@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    # storing token info in this session
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect('/index')

# shows main page - top tracks tracks short term
@app.route('/index')
def index():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect('/')

    sp = spotipy.Spotify(auth=token_info['access_token'])

    # Get the top tracks for the current user
    top_tracks = sp.current_user_top_tracks(time_range = 'short_term', limit=50)

    # Create a DataFrame with the top songs
    df = pd.DataFrame(top_tracks['items'], columns=['name', 'artists', 'popularity'])
    df['artists'] = df['artists'].apply(lambda x: x[0]['name'])

    pop_count_value = pop_count(top_tracks)

    df.index += 1

    #st for short term
    html_table_st = df.to_html(classes=["table"])
    html_table_st = html_table_st.replace('<td>0</td>', '<td></td>')
    html_table_st = html_table_st.replace('<tr style="text-align: right;">', '<tr style="text-align: center;">')
    html_table_st += '<tr><td>Average popularity of the songs in this list: </td><td>{}</td></tr>'.format(pop_count_value)
    # Render the HTML table in the template
    return render_template('index.html', table_st=html_table_st)
        
# get top tracks medium-term
@app.route('/top-tracks-mt')
def top_tracks_mt():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect('/')

    sp = spotipy.Spotify(auth=token_info['access_token'])

    # Get the top tracks for the current user
    top_tracks = sp.current_user_top_tracks(time_range = 'medium_term', limit=50)

    # Create a DataFrame with the top songs
    df = pd.DataFrame(top_tracks['items'], columns=['name', 'artists', 'popularity'])
    df['artists'] = df['artists'].apply(lambda x: x[0]['name'])

    pop_count_value = pop_count(top_tracks)

    df.index += 1

    #mt for medium term
    html_table_mt = df.to_html(classes=["table"])
    html_table_mt = html_table_mt.replace('<td>0</td>', '<td></td>')
    html_table_mt = html_table_mt.replace('<tr style="text-align: right;">', '<tr style="text-align: center;">')
    html_table_mt += '<tr><td>Average popularity of the songs in this list: </td><td>{}</td></tr>'.format(pop_count_value)

    return render_template('top-tracks-mt.html',table_mt=html_table_mt)
 
# display top tracks long-term 
@app.route('/top-tracks-lt')
def top_tracks_lt():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect('/')

    sp = spotipy.Spotify(auth=token_info['access_token'])

     # Get the top tracks for the current user
    top_tracks = sp.current_user_top_tracks(time_range = 'long_term', limit=50)

    # Create a DataFrame with the top songs
    df = pd.DataFrame(top_tracks['items'], columns=['name', 'artists'])
    df['artists'] = df['artists'].apply(lambda x: x[0]['name'])

    df.index += 1

    #lt for long term
    html_table_lt = df.to_html(classes=["table"])
    html_table_lt = html_table_lt.replace('<td>0</td>', '<td></td>')
    html_table_lt = html_table_lt.replace('<tr style="text-align: right;">', '<tr style="text-align: center;">')
    html_table_lt += '<tr><td> Average popularity unavailable </td></tr>'

    return render_template('top-tracks-lt.html', table_lt=html_table_lt)


