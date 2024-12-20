# Import the necessary 

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect, render_template, request, session, url_for
import random


app = Flask(__name__)
app.secret_key = "brazil_zil_zil" 
app.config["SESSION_COOKIE_NAME"] = "mary's_cookie_session"  

# Set up Spotify authentication
sp_oauth = SpotifyOAuth(
    client_id="d8c7c51196a445e688a7ed0840c23f19",  # Replace with your Spotify client ID
    client_secret="e5e2c5db36f143c7aca7dfad5401e77a",  # Replace with your Spotify client secret
    redirect_uri="http://127.0.0.1:5000/callback",  # Add this to your application on the Spotify Developers Dashboard 
    scope="user-top-read"
)

def refresh_spotify_token():
    # Load token from cache
    token_info = sp_oauth.get_cached_token()

    if not token_info or sp_oauth.is_token_expired(token_info):
        try:
            token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
            sp_oauth.save_token_to_cache(token_info)  # Save refreshed token back to cache
            session["token_info"] = token_info
        except Exception as e:
            print(f"Error refreshing token: {e}")
            session.clear()
            return None

    return spotipy.Spotify(auth=token_info["access_token"])


@app.route("/")
def welcome():        #Render the welcome page with a button to login to Spotify.
    token_info = session.get("token_info")
    if token_info:                               # If the user is logged in
        return redirect(url_for("quiz"))         # Redirect to quiz page
    # If not logged in, show the welcome page with login button
    return render_template("welcome.html")


@app.route("/login")
def login():      # Redirect the user to Spotify's authorization page to log in.
    session.clear()           
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# Handle Spotify's callback after user logs in and store the token in the session.

@app.route("/callback")
def callback():           
    token_info = sp_oauth.get_access_token(request.args["code"])
    session["token_info"] = token_info
    return redirect(url_for("quiz"))                        # Redirect to the quiz page after login


@app.route("/logout")
def logout():                          # Remove the token info from the session to log the user out
    session.pop("token_info", None)
    return redirect(url_for("welcome"))  # Redirect to welcome page after logout

@app.route("/quiz")
def quiz():        
    """
    Render the quiz page with dynamically generated questions based on the user's listening habits, 
    interacting with the Spotify API to fetch the user's top tracks and artists for different time ranges 
    (last month, last 6 months, and all time). The data is then organized into quiz questions.

    """
    print("Session before quiz:", session)
    token_info = session.get("token_info")
    if not token_info:
        return redirect(url_for("login"))

    sp = refresh_spotify_token() 
    if sp is None:
        return redirect(url_for("login"))    # Initialize the Spotipy client with the refreshed token.
   

    # Fetch top tracks and artists for different time ranges using Spotify's API:
    
    # Last month (short_term)
    top_tracks_short = sp.current_user_top_tracks(limit=6, time_range="short_term")["items"]
    top_artists_short = sp.current_user_top_artists(limit=6, time_range="short_term")["items"]

    # Last 6 months (medium_term)
    top_tracks_medium = sp.current_user_top_tracks(limit=6, time_range="medium_term")["items"]
    top_artists_medium = sp.current_user_top_artists(limit=6, time_range="medium_term")["items"]

    # All time (long_term)
    top_tracks_long = sp.current_user_top_tracks(limit=6, time_range="long_term")["items"]
    top_artists_long = sp.current_user_top_artists(limit=6, time_range="long_term")["items"]

    # Organize the fetched data into a structured format for quiz questions:
    quiz_data = {
        "song_of_the_year": [track["name"] for track in top_tracks_medium],
        "artist_of_the_year": [artist["name"] for artist in top_artists_medium],
        "song_of_last_month": [track["name"] for track in top_tracks_short],
        "album_of_last_6_months": [
            (
                track["album"]["name"],
                ", ".join(artist["name"] for artist in track["album"]["artists"]),
                track["album"]["images"][0]["url"] if track["album"]["images"] else None
            )
            for track in top_tracks_medium
        ],
        "all_time_artist": [artist["name"] for artist in top_artists_long]
    }

   # Shuffle the options for each question to make the quiz more dynamic.
    for key in quiz_data:
        random.shuffle(quiz_data[key])

     # Render the `quiz.html` template, passing the organized quiz data.
    return render_template(
        "quiz.html",
        quiz_data=quiz_data
    )


@app.route("/quiz_result", methods=["POST", "GET"])
def quiz_result():  
    """
    Process the quiz results, compare user answers with actual Spotify data,
    and render the results page. Also allows the user to explore they own spotify data, 
    rendering their top artists, songs and albums in the different time ranges. 
    """
    user_answers = {             # Retrieve the user's answers from the form 
        "song_of_the_year": request.form.get("song_of_the_year"),
        "artist_of_the_year": request.form.get("artist_of_the_year"),
        "song_of_last_month": request.form.get("song_of_last_month"),
        "album_of_last_6_months": request.form.get("album_of_last_6_months"),
        "all_time_artist": request.form.get("all_time_artist"),
    }

    time_range_labels = {       # Time range labels for Spotify's top items to be displayed later
        "short_term": "Last Month",
        "medium_term": "Last Year",
        "long_term": "All Time",
    }

    token_info = session.get("token_info")                  # Retrieve Spotify token from the session again to make sure it works
    if not token_info or "access_token" not in token_info:
        return redirect(url_for('login'))

    sp = spotipy.Spotify(auth=token_info["access_token"])
    
    try:     # Fetch data for all time ranges for the quiz validation
        short_term_tracks = sp.current_user_top_tracks(limit=6, time_range="short_term")
        medium_term_tracks = sp.current_user_top_tracks(limit=6, time_range="medium_term")
        long_term_tracks = sp.current_user_top_tracks(limit=6, time_range="long_term")

        short_term_artists = sp.current_user_top_artists(limit=6, time_range="short_term")
        medium_term_artists = sp.current_user_top_artists(limit=6, time_range="medium_term")
        long_term_artists = sp.current_user_top_artists(limit=6, time_range="long_term")
    except Exception as e:     #Handle error
        print("Error fetching data from Spotify:", e)
        return redirect(url_for('login'))

    # Extract correct answers based on specific time ranges refered to on each question 
    correct_answers = {    # Extracts the name of the desired track (number 1) from the list of items given by spotify
        "song_of_the_year": medium_term_tracks["items"][0]["name"] if medium_term_tracks["items"] else None,
        "artist_of_the_year": medium_term_artists["items"][0]["name"] if medium_term_artists["items"] else None,
        "song_of_last_month": short_term_tracks["items"][0]["name"] if short_term_tracks["items"] else None,
        "album_of_last_6_months": medium_term_tracks["items"][0]["album"]["name"] if medium_term_tracks["items"] else None,  #Refers to the album of the most listed song
        "all_time_artist": long_term_artists["items"][0]["name"] if long_term_artists["items"] else None,
    }

    #Debugging
    print("Correct Answers:", correct_answers)
    print("Short-Term Tracks:", short_term_tracks)
    print("Medium-Term Artists:", medium_term_artists)


    # Calculate the user's score  
    score = 0
    for key, correct_answer in correct_answers.items():
        if user_answers[key] == correct_answer:
            score += 1

    # Now fetch data to display the user's other Spotify stats, allowing for filtering by time range

    time_range = request.form.get("time_range", "medium_term")           # Maps the selected time range, defaults to medium term if none is selected
    time_range_label = time_range_labels.get(time_range, "Last Year")     

    try:   # Spotify's API calls, limited to 6 for display
        top_tracks_data = sp.current_user_top_tracks(limit=6, time_range=time_range)
        top_tracks = [     # Gets the URL of the top songs' album's cover image (if available)
            {"name": track["name"], "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else None}
            for track in top_tracks_data.get("items", [])     
        ]

        top_artists_data = sp.current_user_top_artists(limit=6, time_range=time_range)
        top_artists = [         # Gets the URL of the top artists' Spotify profile picture
            {"name": artist["name"], "image_url": artist["images"][0]["url"] if artist["images"] else None}
            for artist in top_artists_data.get("items", [])     # Gets the URL of the artist's Spotify profile picture
        ]
 
        top_albums = [         # Gets the URL of the album's cover image
            (
                track["album"]["name"], 
                ", ".join(artist["name"] for artist in track["album"]["artists"]),
                track["album"]["images"][0]["url"] if track["album"]["images"] else None
            )
            for track in top_tracks_data.get("items", [])         
        ]
    except Exception as e:   # Handles errors
        print("Error fetching data for time range:", e)
        top_tracks = []            # Sets top_tracks, top_artists, and top_albums to empty lists to ensure the application continues to run without crashing.
        top_artists = []
        top_albums = []

    
    # Render the quiz result page, "quiz_result.html")
    return render_template(
        "quiz_result.html",
        user_answers=user_answers,
        correct_answers=correct_answers,
        top_tracks=top_tracks,
        top_artists=top_artists,
        top_albums=top_albums,
        score=score,
        time_range=time_range,
        time_range_label=time_range_label
    )


if __name__ == "__main__":  # Run the Flask application in debug mode for development purposes
    app.run(debug=True)
