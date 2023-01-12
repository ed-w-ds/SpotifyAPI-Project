import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

CLIENT_ID="57b04b1761114d7d8343c6b5e37330f9"
CLIENT_SECRET="fe65c3db369a42538e8694d9698d0c47"
AUTH_URL = 'https://accounts.spotify.com/api/token'

def main():

    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    rec = sp.recommendations(seed_artists=["3PhoLpVuITZKcymswpck5b"], seed_genres=["pop"], seed_tracks=["1r9xUipOqoNwggBpENDsvJ"], limit=100)
    for track in rec['tracks']:
        print(track['artists'][0]['name'], track['name'])
        
main()