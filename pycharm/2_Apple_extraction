import schedule
import time
import applemusicpy
from datetime import datetime
import json
from geopy.geocoders import Nominatim

# Opening the Apple secret key
def open_secret_key(secret_key):
    """
    Opens the Apple secret key file and returns its contents.

    Args:
        secret_key (str): Path to the Apple secret key file.

    Returns:
        str: Content of the secret key file.
    """
    with open(secret_key) as f:
        read_secret_key = f.read()
    return read_secret_key


# Opening the Apple's music playlists ids
def open_json_file(playlist_ids):
    """
    Opens the JSON file containing Apple Music playlist IDs and returns its contents.

    Args:
        playlist_ids (str): Path to the JSON file.

    Returns:
        dict: Parsed contents of the JSON file.
    """
    with open(playlist_ids) as json_file:
        data = json.load(json_file)
    return data

# Getting daily Apple's music playlists data and storing it into a JSON file
def get_playlist_info(secret_key, playlist_ids):
    """
    Retrieves daily Apple Music playlists data and stores it in a JSON file.

    Args:
        secret_key (str): Path to the Apple secret key file.
        playlist_ids (str): Path to the JSON file containing playlist IDs.
    """
    read_secret_key = open_secret_key(secret_key)
    read_playlist_ids = open_json_file(playlist_ids)

    list_playlists = list(read_playlist_ids.values())
    am = applemusicpy.AppleMusic(secret_key=read_secret_key, key_id='J3GD4JJR33', team_id='C8PRRUB4C5')
    results = am.playlists(list_playlists)
    dt_string = datetime.now().strftime("%Y-%m-%d_%H%M")
    playlists_data_file_name = 'apple_' + dt_string + '.json'

    with open(playlists_data_file_name, "w") as outfile:
        json.dump(results, outfile)

# Getting geocoordinates from cities in the playlist_ids
def get_coord(playlist_ids):
    """
    Retrieves geocoordinates (latitude and longitude) of cities from a JSON file.

    Args:
        playlist_ids (str): Path to the JSON file containing playlist IDs.

    Returns:
        dict: A dictionary with city names as keys and corresponding coordinates as values.
    """
    read_playlist_ids = open_json_file(playlist_ids)
    list_cities = list(read_playlist_ids.keys())
    geolocator = Nominatim(user_agent="hslu")
    dict_of_coords = {
        location: (geolocator.geocode(location).latitude, geolocator.geocode(location).longitude)
        for location in list_cities
    }
    return dict_of_coords

# Function to be scheduled
def scheduled_job():
    """
    Function to be executed as a scheduled job.
    """
    SECRET_KEY = 'AuthKey_J3GD4JJR33.p8'
    PLAYLIST_IDS = 'playlist_ids.json'
    get_playlist_info(SECRET_KEY, PLAYLIST_IDS)

# Schedule the job to run at 10pm every day
schedule.every().day.at("22:00").do(scheduled_job)

# Keep the script running continuously
while True:
    schedule.run_pending()
    time.sleep(1)
