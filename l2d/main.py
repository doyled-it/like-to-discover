import typer

from .songs import (
    TARGET_PLAYLIST_ID,
    get_discover_weekly_songs,
    get_like_to_discover_songs,
    get_liked_songs,
    sp,
)
from .utils.logger import create_logger

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

log = create_logger(__name__)


@app.callback(
    no_args_is_help=True,
)
def callback():
    """
    Like-to-Discover: A tool to add your liked songs from your Discover Weekly playlist
    to a Like to Discover playlist.
    """
    pass


@app.command(help="Run the Like-to-Discover app")
def run():
    """Run the L2D app"""
    liked_tracks = get_liked_songs()
    discover_weekly_tracks = get_discover_weekly_songs()
    like_to_discover_tracks = get_like_to_discover_songs()

    # Find the intersection of liked songs and Discover Weekly songs
    songs_to_add = list(set(liked_tracks) & set(discover_weekly_tracks))
    # Remove those that are already in the playlist
    songs_to_add = list(set(songs_to_add) - set(like_to_discover_tracks))

    if songs_to_add:
        sp.playlist_add_items(TARGET_PLAYLIST_ID, songs_to_add)
        log.info(f"Added {len(songs_to_add)} songs to the target playlist.")
    else:
        log.info("No new songs to add.")
