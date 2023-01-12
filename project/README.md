# SPOTIFY TOP TRACKS TRACKER - SPOTIFYreview
#### Video Demo: 
#### Description:
SPOTIFYreview is a web application that allows users to view their top tracks over various time periods, including short-term, medium-term, and long-term. It also displays the popularity of each track and the average popularity of the top 50 tracks for the selected time period, as well as the artists of those tracks. This application is implemented using the Flask framework and interacts with the Spotify API to retrieve the requested data.

The create_spotify_oauth function creates an instance of the SpotifyOAuth class from the spotipy library, which handles the authorization process with Spotify. The get_token function checks if there is a stored token in the session, and if it exists, it verifies whether the token has expired. If the token has expired, the function uses the refresh_access_token method of the SpotifyOAuth instance to obtain a new token. The pop_count function calculates the average popularity of the user's top tracks by summing the popularity of each track and dividing the result by the number of tracks.

The routes utilise the Spotify class from the spotipy library to retrieve the user's top tracks and stores the track information in a Pandas DataFrame. The DataFrame is then converted to an HTML table and displayed to the user via a template. The long_term route operates in a similar manner, but it displays the user's long-term top tracks instead.

layout.html includes links to external libraries, such as bootstrap, for styling and functionality, as well as a custom stylesheet and a favicon. The template also has a navbar with dropdown menu options for accessing the user's top tracks over various time periods. The template defines blocks for the page title and main content, which can be filled in by other HTML files that inherit from this template.

 index.html, top-tracks-mt.html and top-tracks-lt.html files inherit from the template in the first file. Each file displays an HTML table with the user's top tracks for a specific time period. The tables are generated from Pandas DataFrames and include the track names, artists, and popularity. Each file also displays the average popularity of the top 50 tracks and a button for accessing the user's top tracks in a different time period.

Tools and languages used: python, javaScript, HTML, CSS, Flask, Spotify API, Pandas (see requirements.txt for all the libraries I used)
