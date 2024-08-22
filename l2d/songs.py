import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Load the environment variables
load_dotenv()
# Define your credentials
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
REFRESH_TOKEN = os.getenv("SPOTIPY_REFRESH_TOKEN")

# Define the scopes
scope = "user-library-read playlist-modify-public"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
)

token_info = sp_oauth.refresh_access_token(REFRESH_TOKEN)

sp = spotipy.Spotify(auth=token_info["access_token"])

# Your Discover Weekly playlist ID and target playlist ID
DISCOVER_WEEKLY_PLAYLIST_ID = os.getenv("DISCOVER_WEEKLY_PLAYLIST_ID")
TARGET_PLAYLIST_ID = os.getenv("TARGET_PLAYLIST_ID")


# Get liked songs
def get_liked_songs() -> list[str]:
    """Get the user's liked songs.

    Returns:
        list[str]: A list of the user's liked songs.
    """
    results = sp.current_user_saved_tracks(limit=100)
    liked_tracks = []
    for item in results["items"]:
        track = item["track"]
        liked_tracks.append(track["id"])
    return liked_tracks


# Get Discover Weekly songs
def get_discover_weekly_songs() -> list[str]:
    """Get the user's Discover Weekly songs.

    Returns:
        list[str]: A list of the user's Discover Weekly songs.
    """
    results = sp.playlist_items(DISCOVER_WEEKLY_PLAYLIST_ID)
    discover_weekly_tracks = []
    for item in results["items"]:
        track = item["track"]
        discover_weekly_tracks.append(track["id"])
    return discover_weekly_tracks


def get_like_to_discover_songs() -> list[str]:
    """Get the user's Like to Discover songs.

    Returns:
        list[str]: A list of the user's Like to Discover songs
    """
    offset = 0
    like_to_discover_tracks = []
    while True:
        results = sp.playlist_items(TARGET_PLAYLIST_ID, offset=offset, limit=100)
        if not results["items"]:
            break
        offset += 100
        for item in results["items"]:
            track = item["track"]
            like_to_discover_tracks.append(track["id"])

    return like_to_discover_tracks
