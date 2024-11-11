import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials from environment variables
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Include scopes for reading saved tracks
scope = "user-library-read"
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
            "pop rap", "pop rock", "pop soul", "spanish pop", "teen pop", "viral pop"],
    "Rock": ["album rock", "alternative rock", "australian rock", "blues rock", "british indie rock", "classic rock", 
             "folk rock", "garage rock", "glam rock", "grunge", "hard rock", "heartland rock", "indie rock", 
             "irish rock", "mexican rock", "modern rock", "punk", "punk rock mexicano", "rock", "rock drums", 
             "rock en espanol", "rock urbano mexicano", "rock-and-roll", "rockabilly", "roots rock", "soft rock"],
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
    "World / International": ["afrobeat", "celtic rock", "colombian pop", "ecuadorian pop", "italian adult pop", 
                              "j-pop", "j-rock", "mexican indie", "nigerian pop", "puerto rican pop", 
                              "spanish pop", "spanish new wave", "spanish pop rock", "vallenato"]
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

# Function to get all genres from the artist IDs and map to general genres with counters
def get_general_genre_to_tracks_map(artist_ids, track_uris, batch_size=50):
    genre_to_tracks = {}
    genre_counter = {}

    for i in range(0, len(artist_ids), batch_size):
        batch = artist_ids[i:i + batch_size]
        artists = sp.artists(batch)['artists']

        for index, artist in enumerate(artists):
            specific_genres = artist['genres']
            general_genre = map_to_general_genre(specific_genres)
            track_uri = track_uris[i + index]

            if general_genre not in genre_to_tracks:
                genre_to_tracks[general_genre] = []
                genre_counter[general_genre] = 0  # Initialize counter

            genre_to_tracks[general_genre].append(track_uri)
            genre_counter[general_genre] += 1  # Increment counter

    return genre_to_tracks, genre_counter

# Main function
def main():
    total_tracks = 1007
    batch_size = 50

    # Get artist IDs and track URIs from the user's saved tracks
    track_uris, artist_ids = get_saved_tracks_artist_ids_and_genres(total_tracks, batch_size)

    # Get the general genre-to-tracks mapping and the counters
    genre_to_tracks, genre_counter = get_general_genre_to_tracks_map(artist_ids, track_uris, batch_size)

    # Print all genres and their counts
    print("General Genre Counts:")
    for genre, count in genre_counter.items():
        print(f"{genre}: {count} tracks")

if __name__ == "__main__":
    main()
