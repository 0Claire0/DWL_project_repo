import json
import os
import psycopg2
import pandas as pd
import requests
import numpy as np
import boto3

# Get the RDS host, database name, username, and password from environment variables
RDS_HOST = os.environ['RDS_HOST']
DB_NAME = os.environ['DB_NAME']
USERNAME_RDS = os.environ['USERNAME_RDS']
PASSWORD_RDS = os.environ['PASSWORD_RDS']

# Initialize the S3 client
s3 = boto3.client('s3')

# Get the S3 bucket name and file name from environment variables
bucket_name = os.environ['S3_BUCKET']
file_lyrics_with_emotions = 'lyrics_with_emotions.csv'

def lambda_handler(event, context):
    # Retrieve the lyrics_with_emotions.csv file from S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_lyrics_with_emotions)
    df = pd.read_csv(obj['Body'])

    try:
        # Connect to the Postgres database
        conn = psycopg2.connect("host={} dbname={} user={} password={}".format(RDS_HOST, DB_NAME, USERNAME_RDS, PASSWORD_RDS))
    except psycopg2.Error as e:
        print("Error: Could not make connection to the Postgres database")
        print(e)

    try:
        # Create a cursor to execute database operations
        cur = conn.cursor()
    except psycopg2.Error as e:
        print("Error: Could not get cursor to the Database")
        print(e)

    # Set autocommit to True
    conn.set_session(autocommit=True)

    # Drop the lyrics_table if it exists
    cur.execute("DROP TABLE IF EXISTS lyrics_table;")

    # Create the lyrics_table
    cur.execute("CREATE TABLE lyrics_table (song_id text, artist_name text, song_name text, lyrics text, anger float, joy float, optimism float, sadness float)")

    try:
        # Insert rows into the lyrics_table
        for index, row in df.iterrows():
            cur.execute("""INSERT INTO lyrics_table (song_id, artist_name, song_name, lyrics, anger, joy, optimism, sadness)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (row['song_id'], row['artist_name'], row['song_name'], row['lyrics'], row['anger'], row['joy'], row['optimism'], row['sadness']))
    except psycopg2.Error as e:
        print("Error: Inserting Rows")
        print(e)

    try:
        # Retrieve all rows from the lyrics_table
        cur.execute("SELECT * FROM lyrics_table;")
    except psycopg2.Error as e:
        print("Error: SELECT *")
        print(e)

    # Fetch and print each row
    row = cur.fetchone()
    while row:
        print(row)
        row = cur.fetchone()

    # Close the cursor and connection
    cur.close()
    conn.close()
