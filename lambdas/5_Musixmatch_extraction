import pandas as pd
import boto3
import csv
import requests
import os

def get_song_info(s3_bucket, s3_key):
    """
    Retrieves song information from a CSV file stored in an S3 bucket.

    Args:
        s3_bucket (str): The name of the S3 bucket.
        s3_key (str): The key (path) of the CSV file in the S3 bucket.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the song information.
    """
    # Set up the S3 client
    s3 = boto3.client('s3')

    # Read the CSV file from S3
    response = s3.get_object(Bucket=s3_bucket, Key=s3_key)
    csv_content = response['Body'].read().decode('utf-8').splitlines()

    # Open the CSV file
    csv_reader = csv.DictReader(csv_content)
    columns_to_extract = ["song_id", "artist_name", "song_name"]

    song_ids = []
    artist_names = []
    song_names = []

    for row in csv_reader:
        song_id = row['song_id']
        artist_name = row['artist_name']
        song_name = row['song_name']

        song_ids.append(song_id)
        artist_names.append(artist_name)
        song_names.append(song_name)

    unique_values = list(set(zip(song_ids, artist_names, song_names)))

    df = pd.DataFrame(unique_values, columns=columns_to_extract)

    return df

def get_lyrics(artist_name, song_name, apikey_musixmatch, apiurl_musixmatch):
    """
    Retrieves lyrics for a given artist and song using the Musixmatch API.

    Args:
        artist_name (str): The name of the artist.
        song_name (str): The name of the song.
        apikey_musixmatch (str): The API key for Musixmatch.
        apiurl_musixmatch (str): The base URL for Musixmatch API.

    Returns:
        str: The lyrics of the song, or an empty string if lyrics are not found.
    """
    query_string = f'{apiurl_musixmatch}matcher.lyrics.get?&q_track={song_name}&q_artist={artist_name}&apikey={apikey_musixmatch}&format=json&f_has_lyrics=1'
    r = requests.get(query_string)
    response_json = r.json()
    if 'message' in response_json and 'body' in response_json['message'] and 'lyrics' in response_json['message']['body'] and 'lyrics_body' in response_json['message']['body']['lyrics']:
        lyrics = response_json['message']['body']['lyrics']['lyrics_body']
        return lyrics
    else:
        return ""

def lambda_handler(event, context):
    """
    AWS Lambda handler function.

    Args:
        event: The event data.
        context: The runtime information of the Lambda function.

    Returns:
        None
    """
    # Specify the S3 bucket and key for the CSV file
    s3_bucket = os.environ['S3_BUCKET']
    s3_key = 'apple_songs.csv'

    # Fetch the song information and create a new DataFrame
    song_df = get_song_info(s3_bucket, s3_key)

    # Add a new column 'lyrics' to the DataFrame
    song_df['lyrics'] = ""

    # Iterate over the rows of the DataFrame
    for index, row in song_df.iterrows():
        artist_name = row['artist_name']
        song_name = row['song_name']

        # Call the get_lyrics function with the artist_name and song_name
        apikey_musixmatch = '1b1821d41b9cb328774a18cdd9fddb27'
        apiurl_musixmatch = 'http://api.musixmatch.com/ws/1.1/'
        lyrics = get_lyrics(artist_name, song_name, apikey_musixmatch, apiurl_musixmatch)

        # Assign the lyrics to the 'lyrics' column in the DataFrame
        song_df.at[index, 'lyrics'] = lyrics

    # Display the first 10 rows of the DataFrame
    print(song_df.head(10))

    # Store the DataFrame back to S3 as a CSV file
    s3 = boto3.client('s3')
    csv_buffer = song_df.to_csv(index=False).encode('utf-8')
    s3.put_object(Body=csv_buffer, Bucket=s3_bucket, Key='songs_with_lyrics.csv')
