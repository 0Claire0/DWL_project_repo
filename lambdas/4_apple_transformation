import boto3
import json
import pandas as pd
import os
import datetime
import re


# Create an S3 client
s3_client = boto3.client('s3')

# Define the S3 bucket
bucket_name = os.environ['S3_BUCKET']
dict_coord_file = 'dict0fcoords.json'

# Lambda handler function
def lambda_handler(event, context):
    """
    Lambda handler function to process JSON files from an S3 bucket, extract song information,
    merge it with city coordinates, and save the result as a CSV file.

    Args:
        event: Lambda event object.
        context: Lambda context object.
    """
    # Initialize an empty list to store the song information
    all_songs = []
    dictofcoord = []

    # Retrieve a list of all the objects in the bucket
    objects = s3_client.list_objects_v2(Bucket=bucket_name)

    # Retrieve the JSON file from the S3 bucket
    response = s3_client.get_object(Bucket=bucket_name, Key=dict_coord_file)

    # Load the JSON data from the response object
    json_data = response['Body'].read().decode('utf-8')

    # Parse the JSON data into a dictionary object
    coord_data = json.loads(json_data)

    # Create a list of tuples for the dataframe rows
    rows = []
    for city, coords in coord_data.items():
        lat, long = coords
        rows.append((city, lat, long))

    # Create a Pandas dataframe from the list of tuples
    df_coord = pd.DataFrame(rows, columns=['city', 'latitude', 'longitude'])


    # Loop through the list of objects and load the JSON files that have "apple" in their name
    for obj in objects['Contents']:
        if 'apple' in obj['Key'] and obj['Key'].endswith('.json'):
            # Retrieve the JSON file from S3
            response = s3_client.get_object(Bucket=bucket_name, Key=obj['Key'])

            # Extract the date from the file name using regular expressions
            match = re.search(r'\d{4}-\d{2}-\d{2}', obj['Key'])
            if match:
                extraction_date = match.group()

            # Load the dictionary from the JSON file
            my_dict = json.loads(response['Body'].read())

            # Loop over each city in the dictionary
            for city_data in my_dict['data']:
                city_name = city_data['attributes']['name'].replace('Top 25: ', '')
                city_songs = city_data['relationships']['tracks']['data']
                last_update = city_data['attributes']['lastModifiedDate']
                last_update = datetime.datetime.strptime(last_update, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")

                # Loop over each song in the city and extract the information
                ranking = 0
                for song in city_songs:
                    ranking += 1
                    song_id = song['id']
                    song_name = song['attributes']['name']
                    artist_name = song['attributes']['artistName']
                    album_name = song['attributes']['albumName']
                    genre = song['attributes']['genreNames']
                    release_date = song['attributes'].get('releaseDate', '')  # use get() method with default value ''
                    duration = song['attributes']['durationInMillis']
                    # ranking = song['attributes']['previews'][0].get('artworkUrl')  # extract ranking from artworkUrl
                    if 'contentRating' in song['attributes']:
                        explicit = song['attributes']['contentRating'] == 'explicit'
                    else:
                        explicit = False

                    # Append the song information to the list
                    all_songs.append({
                        'city': city_name,
                        'last_playlist_update': last_update,
                        'extraction_date' : extraction_date,
                        'ranking': ranking,
                        'song_id': song_id,
                        'song_name': song_name,
                        'artist_name': artist_name,
                        'album_name': album_name,
                        'genre': genre,
                        'release_date': release_date,
                        'duration (ms)': duration,
                        'explicit': explicit
                    })

    # Create a pandas dataframe from the list of songs
    songs_df = pd.DataFrame(all_songs)

    # Merge the two dataframes based on the 'City' column
    merged_df = pd.merge(songs_df, df_coord, on='city')

    # Save the dataframe to a CSV file
    csv_buffer = merged_df.to_csv(index=False)

    # Upload the CSV file to S3
    csv_key = 'apple_songs.csv'
    s3_client.put_object(Bucket=bucket_name, Key=csv_key, Body=csv_buffer)

    print(f"CSV file uploaded to s3://{bucket_name}/{csv_key}")


if __name__ == "__main__":
    # Execute the lambda_handler function when running the script as standalone
    lambda_handler(None, None)
