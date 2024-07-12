# Like-to-Discover

**Like-to-Discover** is a Python-based command-line tool that allows you to automatically move songs you like from your Discover Weekly playlist to another playlist of your choice on Spotify. This project uses the Spotify API and is managed with Poetry for dependency management.

## Features

- Automatically transfer liked songs from Discover Weekly to a target playlist.
- Scheduled execution using GitHub Actions to run every 5 minutes.
- Managed with Poetry for easy dependency management.

## Prerequisites

- Python 3.12 or higher
- A Spotify Developer account with a registered application
- Poetry (for dependency management)
- Docker (optional, for containerized deployment)
- Heroku account (optional, for deployment)

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/doyled-it/like-to-discover.git
cd like-to-discover
```

### 2. Install Dependencies

#### Using Poetry

```sh
poetry install
```

### 3. Spotify API Credentials

Create a Spotify Developer account and register a new application to get your `Client ID`, `Client Secret`, and set a `Redirect URI`.

- Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
- Create a new application.
- Copy the `Client ID` and `Client Secret`.
- Set the `Redirect URI` (e.g., `http://localhost:8888/callback`).

### 4. Environment Variables

Create a `.env` file in the root directory and add your Spotify credentials:

```sh
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
SPOTIPY_REFRESH_TOKEN=your_refresh_token_here
DISCOVER_WEEKLY_PLAYLIST_ID=your_discover_weekly_playlist_id
TARGET_PLAYLIST_ID=your_target_playlist_id
```

#### 4.1 Obtain the Refresh Token

Run the following script to get the initial refresh token:

```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = 'your_client_id_here'
CLIENT_SECRET = 'your_client_secret_here'
REDIRECT_URI = 'http://localhost:8888/callback'
scope = "user-library-read playlist-modify-public"

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=scope)

# Get the URL to authorize the application
auth_url = sp_oauth.get_authorize_url()
print(f"Please navigate to this URL to authorize the application: {auth_url}")

# Prompt the user to paste the redirect URL after authorization
response = input("Paste the redirect URL here: ")

# Extract the code from the redirect URL
code = sp_oauth.parse_response_code(response)
token_info = sp_oauth.get_access_token(code)

print("Access Token:", token_info['access_token'])
print("Refresh Token:", token_info['refresh_token'])
```

#### 4.2 Obtaining the Playlist IDs

1. Open Spotify in your web browser
2. Navigate to your Discover Weekly and Target Playlists
3. Extract the Playlist IDs from the URL:

```
https://open.spotify.com/playlist/<playlist_id>
```

4. Set the environment variables in your `.env` described in section 4.

### 5. Running the Application Locally

```sh
l2d run
```

### 6. Using Docker

#### 6.1 Build and Run with Docker

1. **Build the Docker Image**

```sh
docker build -t like-to-discover .
```

2. **Run the Docker Container**

```sh
docker run -it --rm --env-file .env like-to-discover
```

### 7. Deployment with GitHub Actions

This project uses GitHub Actions to run the task every 5 minutes.

1. **Set Up GitHub Secrets**

Go to your GitHub repository’s settings, then Secrets, and add the following secrets:

- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`
- `SPOTIPY_REFRESH_TOKEN`

2. **Create GitHub Actions Workflow**

Create a `.github/workflows/main.yml` file in your repository:

```yaml
name: Run l2d every 5 minutes

on:
  schedule:
    - cron: "*/5 * * * *" # Every 5 minutes

jobs:
  run-l2d:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install

      - name: Run l2d
        run: |
          poetry run python -m l2d run
```

3. **Commit and Push**

```sh
git add .
git commit -m "Set up GitHub Actions workflow"
git push origin main
```

### 8. Deployment to Heroku (Optional)

If you prefer deploying to Heroku, follow these steps:

1. **Log in to Heroku Container Registry**

```sh
heroku container:login
```

2. **Build, Tag, and Push Docker Image**

```sh
docker build -t like-to-discover .
docker tag like-to-discover registry.heroku.com/like-to-discover/web
docker push registry.heroku.com/like-to-discover/web
```

3. **Release the Docker Image**

```sh
heroku container:release web -a like-to-discover
```

4. **Set Environment Variables on Heroku**

```sh
heroku config:set SPOTIPY_CLIENT_ID=your_client_id_here -a like-to-discover
heroku config:set SPOTIPY_CLIENT_SECRET=your_client_secret_here -a like-to-discover
heroku config:set SPOTIPY_REDIRECT_URI=http://localhost:8888/callback -a like-to-discover
heroku config:set SPOTIPY_REFRESH_TOKEN=your_refresh_token_here -a like-to-discover
```

### 9. Monitor Logs

Check the logs to ensure the application runs as expected:

```sh
heroku logs --tail -a like-to-discover
```

## Contributing

Feel free to open issues or submit pull requests if you find bugs or want to contribute to the project.

## License

This project is licensed under the MIT License.
