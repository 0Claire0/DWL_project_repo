# The role of weather in the tone of Apple Music users’ musical choices

## What is this repo or project?

This repository was created in the context of a school project for the module of Data Warehouse and Data Lake Systems of [the Master in Applied Information and Data Science of the Lucerne University of Applied Sciences and Arts](https://www.hslu.ch/en/lucerne-school-of-business/degree-programmes/master/applied-information-and-data-science/). It aims at getting and connecting information from historic weather of 30 European cities and the lyrics of the daily Apple top 25 playlists from the same cities to confirm the role of weather in the tone of Apple Music users’ musical choices.

The data collected during this project is supposed to be loaded into an Amazon S3 bucket. Moreover, a trigger is used there to get the data daily. If you want to load it somewhere else, you will need, sometimes, to adapt the code accordingly.

## How does it work?

This project is run in a Python 3.8 environment and uses three APIs to access the data : Meteomatics, Apple Music API and Musixmatch. In addition, the playlists’ IDs are collected from this webpage : https://music.apple.com/us/browse/top-charts

### Meteomatics API
This API is used to collect weather data of 30 European cities. An account has to be created, and the credentials are needed when querying the API. More info at: http://meteomatics.com

### Apple Music API
This API is used to collect information regarding the daily Apple « Top 25 » playlists of 30 European cities. As such, it is necessary to join the Apple Developer Program to use the Apple Music API. Once done, the program provides members with an object key, a secret key, a key ID as well as a team ID, leading to a highly-secure process. More info available at: https://developer.apple.com/documentation/applemusicapi/ 

### Musixmatch API
This API is used to collect the lyrics of the songs listed in the playlists. The generated API key is used in the queries to obtain 30% of the songs’ lyrics (limitation being imposed by Musixmatch for the free plan). More info available at: https://developer.musixmatch.com/

### cardiffnlp/twitter-roberta-base-emotion model
In combination with the songs’ lyrics, the cardiffnlp/twitter-roberta-base-emotion model is used to extract the songs’ associated emotion, or mood. More info available at: https://huggingface.co/cardiffnlp/twitter-roberta-base-emotion

### Amazon Web Services (AWS)
This project uses several resources from AWS, namely S3, Lambda functions and layers, EventBridge triggers and RDS. Access to these resources was granted through a student lab role, as part of the module of Data Warehouse and Data Lake Systems of the Master in Applied Information and Data Science of the Lucerne University of Applied Sciences and Arts. More info available at: https://aws.amazon.com/.

### Repository files

The repository contains seventeen files.

- README - current file

To be uploaded into the S3 bucket:

- playlist_ids - file with the playlist ids of each city hard coded

To be run in AWS terminal or Local terminal:

- boto3_layer - to create a layer for each lambda function
- amp_layer - to create a layer for the specific AppleMusic_ingest lambda function
- meteomatics_and_geopy_layer - to create a layer for the specific Meteomatics_ingest lambda function

To be run in AWS Lambda function:

- 1_Meteomatics_extraction - Lambda function to retrieve weather data and store it in an S3 Bucket
- 3_meteo_transformation - Lambda function to clean and merge weather data into a CSV file
- 4_apple_transformation -  Lambda function to merge Apple Music playlist data and create a CSV file
- 5_Musixmatch_extraction - Lambda function to create a CSV file from unique song values and add related lyrics
- 6_lyrics_transformation - Lambda function to clean the lyrics CSV file
- 8_export_weather_RDS
- 9_export_Apple_RDS
- 10_export_lyrics_RDS

To be run in PyCharm:

- 2_Apple_extraction - Python file to extract the Apple Music data
- 7_emotion_extraction - Python file to add associated emotions to unique song values

To be run in R:

- 16_subquestion4_regression

To use in Tableau Prep and Tableau:

- rds_db_credentials

## Who will use this repo or project? 

Despite all the care taken to ensure confidentiality, some information remained difficult to hide. This is why this repository is private and only intended to be shown to our professors.

However, the project’s results are intended to be addressed to various stakeholders, for example:
- Governmental Institutions, the analysis can provide an indicator of the population welfare and mindset
- Mental Health Instances, the analysis can provide insights based on meteorological data as to the possibility of mental relapse for high risk people and could therefore enhance preventive measures
- Musical Platforms, the use of the analysis can provide pattern for musical platform to propose specific playlists to influence the emotional state of listeners

## What is the goal of this project?

This project aims at determining if weather has an influence on the ton of musical choices. The goal is to improve clients purchase experience if we focus on a marketing aspect, but also if we go further into the research the data could be used in terms of emotional and mental health instances. 

However, the main goal of the project is above all to learn, practice and acquire knowledge about datalakes and datawarehouses using AWS services. 

## Authors
- **Claire Bussat** - [GitHub Profile](https://github.com/0Claire0)
- **Camille Cosandier** - [GitHub Profile](https://github.com/geneva-gang-1)
- **Kelly Queiroga** - [GitHub Profile](https://github.com/kellyeq13)
