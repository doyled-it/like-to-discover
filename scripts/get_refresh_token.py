import os

from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
scope = "user-library-read playlist-modify-public"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
)

# Get the URL to authorize the application
auth_url = sp_oauth.get_authorize_url()
print(f"Please navigate to this URL to authorize the application: {auth_url}")

# Prompt the user to paste the redirect URL after authorization
response = input("Paste the redirect URL here: ")

# Extract the code from the redirect URL
code = sp_oauth.parse_response_code(response)
token_info = sp_oauth.get_access_token(code)

print("Access Token:", token_info["access_token"])
print("Refresh Token:", token_info["refresh_token"])
