try:
    import boto3
    import json
    import os
    from datetime import datetime, timedelta
    from geopy.geocoders import Nominatim
    import meteomatics.api as api
    import pandas as pd
    print("All Modules are ok ...")
except Exception as e:
    print("Error in Imports ")

# Configure S3 client and bucket
S3_CLIENT = boto3.client("s3")
S3 = boto3.resource('s3')
S3_BUCKET = os.environ['S3_BUCKET']
OBJECT_JSON_PLAYLIST = os.environ['OBJECT_JSON_PLAYLIST']
USERNAME_METEOMATICS = os.environ['USERNAME_METEOMATICS']
PASSWORD_METEOMATICS = os.environ['PASSWORD_METEOMATICS']

# Reading the playlist IDs list from a JSON file already uploaded to the S3 bucket
def read_bucket_object(object_key, as_json=False):
    """
    Reads an object from the S3 bucket.

    Args:
        object_key (str): The key of the object to read.
        as_json (bool): If True, parses the object content as JSON.

    Returns:
        The content of the object.
    """
    file_content = S3_CLIENT.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read()
    if as_json:
        file_content = json.loads(file_content)
    return file_content
    
# Writing an object to the bucket
def write_bucket_object(object_key, object_value, as_json=False):
    """
    Writes an object to the S3 bucket.

    Args:
        object_key (str): The key of the object to write.
        object_value: The value of the object to write.
        as_json (bool): If True, converts the object value to JSON before writing.
    """
    if as_json:
        object_value = bytes(json.dumps(object_value).encode('UTF-8'))
    S3_CLIENT.put_object(Bucket=S3_BUCKET, Key=object_key, Body=object_value)

# Getting geocoordinates from cities in the playlist_ids
def get_coord(read_playlist_ids):
    """
    Retrieves the geographical coordinates (latitude and longitude) of cities.

    Args:
        read_playlist_ids (dict): A dictionary containing the playlist IDs.

    Returns:
        A dictionary with city names as keys and corresponding coordinates as values.
    """
    list_cities = list(read_playlist_ids.keys())
    geolocator = Nominatim(user_agent="hslu")
    dict_of_coords = {location: (geolocator.geocode(location).latitude, geolocator.geocode(location).longitude) for location in list_cities}
    return dict_of_coords

def get_meteo(dict_of_coords):
    """
    Retrieves meteorological data for cities using their coordinates.

    Args:
        dict_of_coords (dict): A dictionary with city names as keys and corresponding coordinates as values.
    """
    start_date = datetime.utcnow().replace(hour=1, minute=0, microsecond=0)
    end_date = start_date + timedelta(days=1)
    interval = timedelta(hours=1)
    parameters = ['t_max_2m_24h:C', 'precip_24h:mm', 'weather_symbol_24h:idx']
    
    list_df = []
    for city in dict_of_coords:
        df_meteo_city = api.query_time_series([dict_of_coords[city]], start_date, end_date, interval, parameters, USERNAME_METEOMATICS, PASSWORD_METEOMATICS)
        list_df.append(df_meteo_city)

    df_meteo = pd.concat(list_df, axis=0)
    
    dt_string = datetime.now().strftime("%Y-%m-%d_%H%M")
    meteo_data_file_name = 'meteo_' + dt_string + '.csv'
    df_meteo_csv = df_meteo.to_csv(index=True)
    write_bucket_object(meteo_data_file_name, df_meteo_csv, as_json=False)

# Lambda handler function
def lambda_handler(event, context):
    read_playlist_ids = read_bucket_object(OBJECT_JSON_PLAYLIST, as_json=True)
    dict_of_coords = get_coord(read_playlist_ids)
    get_meteo(dict_of_coords)

if __name__ == "__main__":
    lambda_handler(None, None)
