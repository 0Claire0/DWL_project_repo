try:
    import boto3
    import json
    import os
    #import apple-music-python as applemusicpy
    #from apple-music-python import applemusicpy
    #import apple_music_python as applemusicpy
    import applemusicpy
    from datetime import datetime, timedelta
    print("All Modules are ok ...")
    
except Exception as e:
    print("Error in Imports ")


S3_CLIENT = boto3.client("s3")
S3 = boto3.resource('s3')
S3_BUCKET = os.environ['S3_BUCKET']
OBJECT_JSON_PLAYLIST = os.environ['OBJECT_JSON_PLAYLIST']
APPLE_SECRET_KEY = os.environ['APPLE_SECRET_KEY']
KEY_ID = os.environ['KEY_ID']
TEAM_ID = os.environ['TEAM_ID']

# Reading the playlist IDs list from json file already uploaded in S3 bucket
def read_bucket_object(object_key, as_json = False):
    file_content = S3_CLIENT.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read()
    if as_json:
        file_content = json.loads(file_content)
    return file_content
    
# Writing in the bucket
def write_bucket_object(object_key, object_value, as_json = False):
    if as_json:
        object_value = bytes(json.dumps(object_value).encode('UTF-8'))
    S3_CLIENT.put_object(Bucket=S3_BUCKET, Key=object_key, Body=object_value)
    
# Getting daily Apple's music playlists data and storing it into a s3 bucket
def get_playlist_info(read_playlist_ids):
    list_playlists = list(read_playlist_ids.values())
    am = applemusicpy.AppleMusic(secret_key=APPLE_SECRET_KEY, key_id=KEY_ID, team_id=TEAM_ID)
    results = am.playlists(list_playlists)
    dt_string = datetime.now().strftime("%Y-%m-%d_%H%M")
    playlists_data_file_name = 'apple_' + dt_string + '.json'
    write_bucket_object(playlists_data_file_name, results, as_json = True)


# Getting geocoordinates from cities in the playlist_ids
def get_coord(read_playlist_ids):
    from geopy.geocoders import Nominatim
    list_cities = list(read_playlist_ids.keys())
    geolocator = Nominatim(user_agent="hslu")
    dict0fcoords = {location: (geolocator.geocode(location).latitude, geolocator.geocode(location).longitude) for
                    location in list_cities}
    return dict0fcoords


# Reading one apple playlist json file, already uploaded in S3 bucket
def read_apple_playlist_json(apple_playlist_key):
    file_content = S3_CLIENT.get_object(Bucket=S3_BUCKET, Key=apple_playlist_key)["Body"].read()
    file_content = json.loads(file_content)
    return file_content

# Lambda handler function
def lambda_handler(event, context):
    read_playlist_ids = read_bucket_object(OBJECT_JSON_PLAYLIST, as_json = True)
    get_playlist_info(read_playlist_ids)
    print("tout va bien")


if __name__ == "__main__":
    lambda_handler(None, None)
