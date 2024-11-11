import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Initialize Spotipy client with OAuth
# Include scopes for creating and modifying playlists
scope = "user-top-read playlist-modify-public playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
))

# Function to create with Top 50 songs 
def create_playlists_by_genre(track_uris, user_id):
    playlist = sp.user_playlist_create(user_id, "My Top 50 Songs", public=True)
    playlist_id = playlist['id']
    # Add tracks to the playlist
    sp.playlist_add_items(playlist_id, track_uris)
    print("Playlist 'My Top 50 Songs' created successfully!")

# Function to get the user's top 50 tracks
def get_top_tracks(limit=50):
    user_id = sp.current_user()['id']
    # You can adjust the time range: 'short_term' (4 weeks), 'medium_term' (6 months), 'long_term' (several years)
    results = sp.current_user_top_tracks(limit=limit, time_range='medium_term')
    top_tracks = results['items']
    track_uris = [track['uri'] for track in top_tracks]  # Collect track URIs
    create_playlists_by_genre(track_uris, user_id)
    
    print(f"Your Top {len(top_tracks)} Tracks:")
    for idx, track in enumerate(top_tracks, start=1):
        print(f"{idx}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")

if __name__ == "__main__":
    get_top_tracks()
