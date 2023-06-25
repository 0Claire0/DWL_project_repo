import boto3
import pandas as pd
import os
import re

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

s3 = boto3.client('s3')

bucket_name = os.environ['S3_BUCKET']
lyrics = 'songs_with_lyrics.csv'

def delete_empty_rows(lyrics_df):
    """
    Deletes rows with empty lyrics from the DataFrame.

    Args:
        lyrics_df (pd.DataFrame): The DataFrame containing the lyrics.

    Returns:
        pd.DataFrame: The DataFrame with empty rows removed.
    """
    return lyrics_df.dropna(subset=['lyrics'])

def remove_specific_string(df):
    """
    Removes specific string pattern and everything after it from the lyrics.

    Args:
        df (pd.DataFrame): The DataFrame containing the lyrics.

    Returns:
        pd.DataFrame: The DataFrame with specific string removed.
    """
    df['lyrics'] = df['lyrics'].str.split(r'\n\.\.\.\n\n\*{7}.*').str[0]
    df = df.dropna()
    df = df.reset_index(drop=True)
    return df

def count_caracters(lyrics_df):
    """
    Prints the total number of characters in the lyrics.

    Args:
        lyrics_df (pd.DataFrame): The DataFrame containing the lyrics.

    Returns:
        None
    """
    lyrics_df['Longueur'] = lyrics_df['lyrics'].str.len()
    nombre_total_caracteres = lyrics_df['Longueur'].sum()
    print("Nombre total de caractères :", nombre_total_caracteres)

def lambda_handler(event, context):
    """
    AWS Lambda handler function.

    Args:
        event: The event data.
        context: The runtime information of the Lambda function.

    Returns:
        None
    """
    obj = s3.get_object(Bucket=bucket_name, Key=lyrics)
    df = pd.read_csv(obj['Body'])
    df = delete_empty_rows(df)
    df = remove_specific_string(df)
    count_caracters(df)
    print(df.head(10))

    csv_buffer = df.to_csv(index=False)
    csv_key = 'cleaned_lyrics.csv'
    s3.put_object(Bucket=bucket_name, Key=csv_key, Body=csv_buffer)

    print(f"CSV file uploaded to s3://{bucket_name}/{csv_key}")

if __name__ == "__main__":
    lambda_handler(None, None)
