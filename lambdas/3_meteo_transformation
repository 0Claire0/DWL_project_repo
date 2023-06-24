import os
import csv
import boto3
import json
from datetime import datetime

# S3 bucket name
S3_BUCKET = os.environ['S3_BUCKET']

def get_city_names():
    """
    Retrieve city names from a JSON file stored in an S3 bucket.

    Returns:
        list: List of city names.
    """
    # Read the JSON file from S3 bucket
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=S3_BUCKET, Key='dict0fcoords.json')
    json_data = response['Body'].read().decode('utf-8')

    # Parse the JSON data
    data = json.loads(json_data)
    return list(data.keys())

def lambda_handler(event, context):
    """
    Lambda handler function to merge CSV files and upload the output to an S3 bucket.

    Args:
        event: Lambda event object.
        context: Lambda context object.

    Returns:
        dict: Response object containing the status code and message.
    """
    # List to store filtered rows
    filtered_rows = []

    # Set to store unique coordinates
    unique_coords = set()

    # Iterate over the CSV files in the S3 bucket
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(S3_BUCKET)
    for obj in bucket.objects.filter(Prefix='meteo_'):
        if obj.key.endswith('.csv'):
            # Read the CSV file
            response = obj.get()
            csv_data = response['Body'].read().decode('utf-8')
            csv_reader = csv.reader(csv_data.splitlines(), delimiter=',')
            rows = list(csv_reader)

            # Filter rows to keep only those with time at 08:00:50+00:00
            filtered_rows.extend([row for row in rows if row[2].split(' ')[-1].startswith('08:00:')])

            # Extract unique coordinates
            coords = [(float(row[0]), float(row[1])) for row in filtered_rows]
            unique_coords.update(coords)

    # Get city names from the JSON file
    city_names = get_city_names()

    # Repeat city names for each row in the CSV
    repeated_city_names = []
    for _ in range(len(filtered_rows)):
        repeated_city_names.extend(city_names)

    # Create a CSV file containing the filtered rows with repeated city names and Date column
    output_rows = []
    for i, row in enumerate(filtered_rows):
        lat, lon = float(row[0]), float(row[1])
        city = repeated_city_names[i]
        valid_date = row[2].split(' ')[0]  # Extract the date from ValidDate column
        date = datetime.strptime(valid_date, '%Y-%m-%d').strftime('%Y-%m-%d')  # Format the date
        new_row = [city, lat, lon, date] + row[2:5]  # Add Date column before ValidDate
        output_rows.append(new_row)

    # Write the data to an output file
    output_file = '/tmp/merged_data.csv'
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['city', 'lat', 'lon', 'date', 'validdate', 't_max_2m_24h:C', 'precip_24h:mm'])
        writer.writerows(output_rows)

    # Upload the output file to the S3 bucket
    s3 = boto3.client('s3')
    s3.upload_file(output_file, S3_BUCKET, 'full_weather.csv')

    return {
        'statusCode': 200,
        'body': 'CSV files merged successfully.'
    }

if __name__ == "__main__":
    lambda_handler(None, None)
