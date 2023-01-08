# The role of weather in the tone of Apple Music users’ musical choices

## What is this repo or project?

This repository was created in the context of a school project for the module of Data Warehouse and Data Lake Systems of [the Master in Applied Information and Data Science of the Lucerne University of Applied Sciences and Arts](https://www.hslu.ch/en/lucerne-school-of-business/degree-programmes/master/applied-information-and-data-science/). It aims at getting and connecting information from historic weather of 30 European cities and the lyrics of the daily Apple top 25 playlists from the same cities to confirm the role of weather in the tone of Apple Music users’ musical choices.

The data collected during this project is supposed to be loaded into an Amazon S3 bucket. Moreover, a trigger is used there to get the data daily. If you want to load it somewhere else, you will need to adapt the code accordingly.

## How does it work?

This project uses three APIs to access the data : Meteomatics, Apple Music API and Musixmatch. In addition, the playlists’ IDs are collected from this webpage : https://music.apple.com/us/browse/top-charts

### Meteomatics API
This API is used to collect weather data of 30 European cities. An account has to be created, and the credentials are needed when querying the API. More info at: http://meteomatics.com

### Apple Music API
This API is used to collect information regarding the daily Apple « Top 25 » playlists of 30 European cities. As such, it is necessary to join the Apple Developer Program to use the Apple Music API. Once done, the program provides members with an object key, a secret key, a key ID as well as a team ID, leading to a highly-secure process. More info available at: https://developer.apple.com/documentation/applemusicapi/ 

### Musixmatch API
This API is used to collect the lyrics of the songs listed in the playlists. The generated API key is used in the queries to obtain 30% of the songs’ lyrics (limitation being imposed by Musixmatch for the free plan). More info available at: https://developer.musixmatch.com/

### text2emotion library
In combination with the songs’ lyrics, the text2emotion Python library is used to extract the songs’ associated emotion, or mood. More info available at: https://pypi.org/project/text2emotion/ 

### Amazon Web Services (AWS)
This project uses several resources from AWS, namely S3, Lambda functions and layers, EventBridge triggers and Redshift. Access to these resources was granted through a student lab role, as part of the module of Data Warehouse and Data Lake Systems of the Master in Applied Information and Data Science of the Lucerne University of Applied Sciences and Arts. More info available at: https://aws.amazon.com/.

### Repository files

The repository contains eight Python files.

1. README - current file

To be uploaded into the S3 bucket

2. playlist_ids - file with the playlist ids of each city hard coded

To be run in AWS terminal or Local terminal

3. boto3_layer - to create a layer for each lambda function
4. amp_layer - to create a layer for the specific AppleMusic_ingest lambda function
5. meteomatics_and_geopy_layer - to create a layer for the specific Meteomatics_ingest lambda function

To be run in AWS lambda function

6. AppleMusic_ingest - lambda function to put the Apple Music playlists data into the S3 Bucket
7. Meteomatics_ingest - lambda function to put the weather data into the S3 Bucket
8. Musixmatch_ingest - lambda function to put the lyrics data into the S3 Bucket

To be run in Redshift query console


## Who will use this repo or project? 

Despite all the care taken to ensure confidentiality, some information remained difficult to hide. This is why this repository is private and only intended to be shown to our professors.

However, the project’s results are intended to be addressed to various stakeholders, for example:
- Physical stores, as part of the selection of their background music, to be played for customers
- Musical streaming companies, as part of their recommendation algorithms, to take into account the local weather

## What is the goal of this project?

This project aims at determining if weather has an influence on the ton of musical choices. The goal is to improve clients purchase experience if we focus on a marketing aspect, but also if we go further into the research the data could be used in terms of emotional and mental health instances. 

However, the main goal of the project is above all to learn, practice and acquire knowledge about datalakes and datawarehouses using AWS services. 

## Authors
- **Claire Bussat** - [GitHub Profile](https://github.com/0Claire0)
- **Camille Cosandier** - [GitHub Profile](https://github.com/geneva-gang-1)
- **Kelly Queiroga** - [GitHub Profile](https://github.com/kellyeq13)
