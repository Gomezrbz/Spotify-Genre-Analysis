import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials from environment variables
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Include scopes for reading saved tracks and creating/modifying playlists
scope = "user-library-read playlist-modify-public playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
))

# General genre mapping
GENRE_MAPPING = {
    "Pop": ["acoustic pop", "australian pop", "candy pop", "canadian pop", "dance pop", "europop", "indie pop", 
            "italian pop", "k-pop", "latin pop", "pop", "pop dance", "pop emo", "pop house", "pop punk", 
            "pop rap", "pop soul", "spanish pop", "teen pop", "viral pop", "j-pop","nigerian pop", "puerto rican pop","spanish pop", 
            "colombian pop", "ecuadorian pop", "italian adult pop"],
    "Rock": ["album rock", "alternative rock", "australian rock", "blues rock", "british indie rock", "classic rock", 
             "folk rock", "garage rock", "glam rock", "grunge", "hard rock", "heartland rock", "indie rock", 
             "irish rock", "mexican rock", "modern rock", "punk", "punk rock mexicano", "rock", "rock drums", 
             "rock en espanol", "rock urbano mexicano", "rock-and-roll", "rockabilly", "roots rock", "soft rock", "pop rock", "j-rock","spanish pop rock", "celtic rock" ],
    "Hip Hop / Rap": ["atl hip hop", "australian hip hop", "chicago rap", "conscious hip hop", "contemporary r&b", 
                      "crunk", "detroit hip hop", "dfw rap", "dirty south rap", "dmv rap", "east coast hip hop", 
                      "hardcore hip hop", "hip hop", "hip pop", "lgbtq+ hip hop", "miami hip hop", "melodic rap", 
                      "mexican hip hop", "nyc rap", "oakland hip hop", "old school atlanta hip hop", 
                      "puerto rican rap", "queens hip hop", "rap", "rap conciencia", "rap metal", "rap rock", 
                      "seattle hip hop", "southern hip hop", "spanish hip hop", "trap", "trap argentino", 
                      "trap latino", "underground hip hop", "uk hip hop", "urban contemporary"],
    "R&B / Soul": ["afro r&b", "canadian contemporary r&b", "contemporary r&b", "neo soul", "pop soul", "r&b", "soul"],
    "Electronic / Dance": ["australian dance", "big room", "belgian edm", "complextro", "dance pop", "dance rock", 
                           "edm", "electro", "electro house", "electro latino", "electropop", "electronic rock", 
                           "electronic trap", "europop", "filter house", "house", "melbourne bounce", "moombahton", 
                           "progressive electro house", "progressive house", "slap house", "tropical house", "uk dance"],
    "Country": ["alternative country", "classic country pop", "contemporary country", "country", "country dawn", 
                "country pop", "country road", "deathgrass", "modern country pop", "modern country rock"],
    "Latin": ["bachata", "banda", "bolero", "brazilian hip hop", "corrido", "corridos tumbados", "grupera", 
              "latin afrobeat", "latin alternative", "latin hip hop", "latin pop", "latin rock", "mariachi", 
              "musica chihuahuense", "musica mexicana", "norteno", "ranchera", "reggaeton", "reggaeton colombiano", 
              "sierreno", "urbano latino", "urbano mexicano", "vallenato"],
    "Metal / Hard Rock": ["alternative metal", "birmingham metal", "comic metal", "glam metal", "hardcore hip hop", 
                          "industrial metal", "metal", "miami metal", "nu metal", "rap metal"],
    "Folk / Acoustic": ["acoustic cover", "folk", "folk rock", "folk-pop", "modern folk rock", "neo-folk", "stomp and holler"],
    "Jazz / Blues": ["blues", "blues rock", "jazz pop", "smooth jazz"],
    "Soundtrack / Themes": ["anime", "anime latino", "anime lo-fi", "broadway", "comic", "movie tunes", 
                            "orchestral soundtrack", "scorecore", "show tunes", "theme", "video game music"],
    "Classical": ["a cappella", "baroque pop", "chamber pop", "classical", "orchestral"],
    "Reggae / Ska": ["bossbeat", "reggae fusion", "virgin islands reggae"],
    "World / International": ["afrobeat",
                            "mexican indie", 
                               "spanish new wave","vallenato"]
}

# Function to map specific genres to general genres
def map_to_general_genre(specific_genres):
    for general_genre, detailed_genres in GENRE_MAPPING.items():
        for genre in specific_genres:
            if genre in detailed_genres:
                return general_genre
    return "Other"  # Fallback category for uncategorized genres

# Function to get saved tracks in batches of 50 and extract artist IDs
def get_saved_tracks_artist_ids_and_genres(total_tracks=1007, batch_size=50):
    track_uris = []
    artist_ids = []
    offset = 0

    while offset < total_tracks:
        results = sp.current_user_saved_tracks(limit=batch_size, offset=offset)
        items = results['items']

        if not items:
            break

        for item in items:
            track = item['track']
            artist_id = track['artists'][0]['id']
            track_uris.append(track['uri'])
            artist_ids.append(artist_id)

        offset += batch_size

    return track_uris, artist_ids

# Function to get all genres from the artist IDs and map to general genres
def get_general_genre_to_tracks_map(artist_ids, track_uris, batch_size=50):
    genre_to_tracks = {}

    for i in range(0, len(artist_ids), batch_size):
        batch = artist_ids[i:i + batch_size]
        artists = sp.artists(batch)['artists']

        for index, artist in enumerate(artists):
            specific_genres = artist['genres']
            general_genre = map_to_general_genre(specific_genres)
            track_uri = track_uris[i + index]

            if general_genre not in genre_to_tracks:
                genre_to_tracks[general_genre] = []
            genre_to_tracks[general_genre].append(track_uri)

    return genre_to_tracks

# Function to check if a playlist already exists
def check_playlist_exists(playlist_name):
    user_id = sp.current_user()['id']
    playlists = sp.user_playlists(user_id)
    for playlist in playlists['items']:
        if playlist['name'].lower() == playlist_name.lower():
            return playlist['id']
    return None

# Function to create or update playlists and add tracks in batches of 100
def create_or_update_genre_playlists(genre_to_tracks):
    status = {}

    for genre, uris in genre_to_tracks.items():
        try:
            print(f"Processing genre: {genre}...")

            if not uris:
                status[genre] = "No tracks to add."
                print(f"{genre}: No tracks to add.")
                continue

            # Check if the playlist already exists
            playlist_id = check_playlist_exists(genre)
            if playlist_id:
                status[genre] = "Playlist already exists. Adding tracks."
                print(f"{genre}: Playlist already exists. Adding tracks.")
            else:
                # Create a new playlist
                user_id = sp.current_user()['id']
                playlist = sp.user_playlist_create(user_id, genre, public=True)
                playlist_id = playlist['id']
                status[genre] = "Playlist created successfully."
                print(f"{genre}: Playlist created successfully.")

            # Add tracks to the playlist in batches of 100
            for i in range(0, len(uris), 100):
                batch = uris[i:i + 100]
                sp.playlist_add_items(playlist_id, batch)
                print(f"{genre}: Added batch of {len(batch)} tracks.")

        except Exception as e:
            status[genre] = f"Error: {str(e)}"
            print(f"{genre}: Error - {str(e)}")

    return status

# Main function
def main():
    total_tracks = 1007
    batch_size = 50

    # Get artist IDs and track URIs from the user's saved tracks
    track_uris, artist_ids = get_saved_tracks_artist_ids_and_genres(total_tracks, batch_size)

    # Get the general genre-to-tracks mapping
    genre_to_tracks = get_general_genre_to_tracks_map(artist_ids, track_uris, batch_size)

    # Create or update genre playlists and get the status
    playlist_status = create_or_update_genre_playlists(genre_to_tracks)

    # Print the final status of each playlist
    print("\nSummary of Playlist Creation/Update:")
    for genre, message in playlist_status.items():
        print(f"{genre}: {message}")

if __name__ == "__main__":
    main()
