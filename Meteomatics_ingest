try:
    import boto3
    import json
    import os
    from datetime import datetime, timedelta
    from geopy.geocoders import Nominatim
    import meteomatics.api as api
    print("All Modules are ok ...")
    
except Exception as e:
    print("Error in Imports ")


S3_CLIENT = boto3.client("s3")
S3 = boto3.resource('s3')
S3_BUCKET = os.environ['S3_BUCKET']
OBJECT_JSON_PLAYLIST = os.environ['OBJECT_JSON_PLAYLIST']
USERNAME_METEOMATICS = os.environ['USERNAME_METEOMATICS']
PASSWORD_METEOMATICS = os.environ['PASSWORD_METEOMATICS']


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


# Getting geocoordinates from cities in the playlist_ids
def get_coord(read_playlist_ids):
    list_cities = list(read_playlist_ids.keys())
    geolocator = Nominatim(user_agent="hslu")
    dict0fcoords = {location: (geolocator.geocode(location).latitude, geolocator.geocode(location).longitude) for location in list_cities}
    return dict0fcoords


# Getting meteo data for each city
def get_meteo(dict0fcoords):
    startdate = datetime.utcnow().replace(hour=1, minute=0, microsecond=0)
    enddate = startdate + timedelta(days=1)
    interval = timedelta(hours=1)
    parameters = ['t_max_2m_24h:C', 'precip_24h:mm', 'weather_symbol_24h:idx']
    df_meteo = api.query_time_series(list(dict0fcoords.values()), startdate, enddate, interval, parameters,
                                     USERNAME_METEOMATICS, PASSWORD_METEOMATICS)
    dt_string = datetime.now().strftime("%Y-%m-%d_%H%M")
    meteo_data_file_name = 'meteo_' + dt_string + '.csv'
    df_meteo_csv = df_meteo.to_csv(index=True)
    write_bucket_object(meteo_data_file_name, df_meteo_csv, as_json = False)

# Lambda handler function
def lambda_handler(event, context):
    read_playlist_ids = read_bucket_object(OBJECT_JSON_PLAYLIST, as_json = True)
    dict0fcoords = get_coord(read_playlist_ids)
    get_meteo(dict0fcoords)

if __name__ == "__main__":
    lambda_handler(None, None)
