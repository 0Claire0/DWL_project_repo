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


# list the bucket files that start with "apple"
def list_files_names():
    bucket = S3.Bucket(S3_BUCKET)
    all_objs = bucket.objects.all()
    list_files_names = []
    for obj in all_objs:
        if obj.key.startswith('apple'):
            list_files_names.append(obj.key)
    print(list_files_names)
    return list_files_names


# Reading the playlist infos from json files already uploaded in S3 bucket
def read_bucket_object(object_key, as_json = False):
    file_content = S3_CLIENT.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read()
    if as_json:
        file_content = json.loads(file_content)
    return file_content



def get_loc(playlist_info_all_days):

    column_city_list = []
    column_date_list = []
    column_song_name_list = []
    column_artist_name_list = []
    column_genre_list = []

    for day in range(len(playlist_info_all_days)):
        for playlist in playlist_info_all_days[day]['data']:
            city_name = playlist['attributes']['name'].split(" ", 2)[2]
            column_city_list.append(city_name)

            last_modified_date = playlist['attributes']['lastModifiedDate'].rsplit("T", 1)[0]
            column_date_list.append(last_modified_date)

            for song in playlist['relationships']['tracks']['data']:
                song_name = song['attributes']['name']
                column_song_name_list.append(song_name)

                artist_name = song['attributes']['artistName']
                column_artist_name_list.append(artist_name)

                genre = song['attributes']['genreNames']
                column_genre_list.append(genre)

    column_city_list_all = []
    for city in column_city_list:
        for i in range(25):
            column_city_list_all.append(city)

    column_date_list_all = []
    for i in column_date_list:
        counter = 0
        while counter < 25:
            column_date_list_all.append(i)
            counter += 1

    # ranking = [str(i) for i in range(1,26)]
    column_ranking_all = []

    
    

    counter = 0
    while counter < 330:
        column_ranking_all.extend([str(i) for i in range(1,26)])
        counter += 1
    print(column_ranking_all)
    
    print(len(column_ranking_all))
    print(len(column_city_list_all))
    print(len(column_date_list_all))
    print(len(column_song_name_list))
    print(len(column_artist_name_list))
    print(len(column_genre_list))
    
    


    data = {'index': column_ranking_all, 'date' : column_date_list_all, 'city' : column_city_list_all, 'song_name': column_song_name_list, 'artist_name' : column_artist_name_list}
    df = pd.DataFrame(data)
    print(df)
    return df
    
    
# writing in the bucket
def write_bucket_object(object_key, object_value, as_json = False):
    if as_json:
        object_value = bytes(json.dumps(object_value).encode('UTF-8'))
    S3_CLIENT.put_object(Bucket=S3_BUCKET, Key=object_key, Body=object_value)
    

# Lambda handler function
def lambda_handler(event, context):
    playlist_info_all_days = []
    for playlist_info_daily in list_files_names():
        read_playlist_info = read_bucket_object(playlist_info_daily, as_json = True)
        playlist_info_all_days.append(read_playlist_info)
        
    big_apple_file_all_days_df = get_loc(playlist_info_all_days)

    
    dt_string = datetime.now().strftime("%Y-%m-%d_%H%M")
    file_name = 'big_apple_file_all_days_' + dt_string + '.csv'
    big_apple_csv = big_apple_file_all_days_df.to_csv(index=True)
    write_bucket_object(file_name, big_apple_csv, as_json = False)


if __name__ == "__main__":
    lambda_handler(None, None)
    
