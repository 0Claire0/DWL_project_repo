try:
    import boto3
    import json
    import os
    import pandas as pd
    from datetime import datetime
    print("All Modules are ok ...")
    
except Exception as e:
    print("Error in Imports ")


S3_CLIENT = boto3.client("s3")
S3 = boto3.resource('s3')
S3_BUCKET = os.environ['S3_BUCKET']
OBJECT_JSON_PLAYLIST = os.environ['OBJECT_JSON_PLAYLIST']


# Reading a json file from the bucket
def read_bucket_json_object(object_key):
    file_content = S3_CLIENT.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read()
    file_content = json.loads(file_content)
    return file_content

# Reading a csv file from the bucket
def read_bucket_csv_object(object_key):
    file_content = S3_CLIENT.get_object(Bucket=S3_BUCKET, Key=object_key)
    df_file_content = pd.read_csv(file_content.get("Body"))
    return df_file_content

# writing in the bucket
def write_bucket_object(object_key, object_value, as_json = False):
    if as_json:
        object_value = bytes(json.dumps(object_value).encode('UTF-8'))
    S3_CLIENT.put_object(Bucket=S3_BUCKET, Key=object_key, Body=object_value)
    
# list the bucket files that start with "meteo"
def list_files_names():
    bucket = S3.Bucket(S3_BUCKET)
    all_objs = bucket.objects.all()
    list_files_names = []
    for obj in all_objs:
        if obj.key.startswith('meteo'):
            list_files_names.append(obj.key)
    return list_files_names

# This function takes the first date of each CSV file and put it on a list * the number of cities
def get_dates(read_df_meteo):
    list_dates = []
    date = read_df_meteo.iloc[0][2]
    date = date.split()[0]
    for i in (read_df_meteo['lat'].unique()):
        list_dates.append(date)
    return list_dates

# This function gets the mean temperature for each city
def get_mean_temp(df_meteo):
    list_temp = []
    for coord in (df_meteo['lat'].unique()):
        list_temp.append(round((df_meteo['t_max_2m_24h:C'].where(df_meteo['lat'] == coord).dropna()).mean(),2))
    return list_temp

# This function gets the mean precipitation for each city
def get_mean_precip(df_meteo):
    list_precip = []
    for coord in (df_meteo['lat'].unique()):
        list_precip.append(round((df_meteo['precip_24h:mm'].where(df_meteo['lat'] == coord).dropna()).mean(),2))
    return list_precip
    
# get the most frequent value for weather symboles
def get_mode(df_meteo):
    list_mode = []
    for coord in (df_meteo['lat'].unique()):
        list_mode.append(df_meteo['weather_symbol_24h:idx'].where(df_meteo['lat'] == coord).value_counts().idxmax())
    return list_mode

# create a daily meteo df with the values we are interested in
def create_daily_meteo_df(list_dates, list_mean_temp, list_mean_precip, list_mode):
    list_cities = list(read_bucket_json_object(OBJECT_JSON_PLAYLIST).keys())
    data = {'city': list_cities, 'date' : list_dates, 'mean_temp' : list_mean_temp, 'mean_precip': list_mean_precip, 'weather_symbol' : list_mode}
    df = pd.DataFrame(data)
    return df


# Lambda handler function
def lambda_handler(event, context):
    data = {'city': [], 'date' : [], 'mean_temp' : [], 'mean_precip': [], 'weather_symbol' : []}
    weather_all_days_df = pd.DataFrame(data)  
    # ouvrir le big csv ici et à la fin du for, append to le csv
    for df_meteo in list_files_names():
        read_df_meteo = read_bucket_csv_object(df_meteo)
        list_dates = get_dates(read_df_meteo)
        list_mean_temp = get_mean_temp(read_df_meteo)
        list_mean_precip = get_mean_precip(read_df_meteo)
        list_mode = get_mode(read_df_meteo)
        daily_meteo_df = create_daily_meteo_df(list_dates, list_mean_temp, list_mean_precip, list_mode)
        weather_all_days_df = weather_all_days_df.append(daily_meteo_df)
    print(weather_all_days_df)
    dt_string = datetime.now().strftime("%Y-%m-%d_%H%M")
    weather_all_days_df_file_name = 'weather_all_days_' + dt_string + '.csv'
    weather_all_days_csv = weather_all_days_df.to_csv(index=True)
    write_bucket_object(weather_all_days_df_file_name, weather_all_days_csv, as_json = False)

if __name__ == "__main__":
    lambda_handler(None, None)
