Spotify Genre Analysis
======================

This project is designed to retrieve all genres from a user's saved tracks on Spotify and map them to broader, general genres. It then counts the number of tracks in each general genre and displays the results.

What the Code Does
------------------

1.  **Retrieves Saved Tracks**: The code connects to the Spotify API and fetches the user's saved tracks in batches of 50.
    
2.  **Maps Specific Genres to General Genres**: Using a predefined mapping, the code categorizes specific Spotify genres into broader general genres (e.g., "dance pop" becomes "Pop").
    
3.  **Counts Tracks by Genre**: The code counts the number of tracks in each general genre and outputs these counts.
    
4.  **Environment Setup**: The script requires Spotify API credentials to authenticate and fetch data from the user's library.
    

Prerequisites
-------------

*   **Python**: Make sure Python is installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).
    
*   bashCopiar códigopip install spotipy
    
*   **Spotify Developer Account**: You need a Spotify Developer account to obtain API credentials. Sign up at [Spotify Developer](https://developer.spotify.com/).
    

Things Needed to Run the Code
-----------------------------

1.  You can get these by creating an application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
    
    *   **Client ID**
        
    *   **Client Secret**
        
    *   **Redirect URI**
        
2.  **Environment Variables**: The script requires environment variables to securely store your Spotify API credentials.
    

Environment Variables
---------------------

Set up the following environment variables on your system:

*   SPOTIFY\_CLIENT\_ID: Your Spotify API client ID.
    
*   SPOTIFY\_CLIENT\_SECRET: Your Spotify API client secret.
    
*   SPOTIFY\_REDIRECT\_URI: Your Spotify API redirect URI.
    

Links Used
----------

*   [**Spotipy Documentation**](https://spotipy.readthedocs.io/): Documentation for the Spotipy library used to interact with the Spotify API.
    
*   [**Spotify Developer API**](https://developer.spotify.com/): Official documentation for the Spotify Web API, used for fetching user data and managing playlists.