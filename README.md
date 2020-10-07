# Project: Data Modeling with Postgres
## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Datasets
### Song Dataset
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. 

### Log Dataset
The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

## Project Description

In order for Sparkify to be able to store this above mentioned data in a structured way and in order for them to be able to run analytics on this data, the data has to be moved from a flatfile format into an RDBMS. We will be organizing the data into a fact table connected to multiple normalized dimension tables as a star schema. We will write an ETL pipeline to read the files one by one into dataframes, the data relevant for each dimension table is extracted and then inserted into the database tables. 

The key facts that is contained in the data is the song play activity that is contained in the logs. All other data can be separated into songs, artist, and user related information. In order to make analysis easier we will also breakdown the timestamp related information into its own table so that is it is easier to aggregated based on datetime breakups. With this data, we will be able to run queries such as most popular songs, most popular artists, analyse playtimes by users and so on.

## Databases

### Fact Table

### songplays
+ songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
+ 6820 records

### Dimension Tables

#### artists
+ artist_id, name, location, latitude, longitude
+ 69 records

#### songs
+ song_id, title, artist_id, year, duration
+ 71 records

#### users
+ user_id, first_name, last_name, gender, level
+ 96 records 

#### time
+ start_time, hour, day, week, month, year, weekday
+ 6813 records

## Data Analysis - sample questions

### Q: What were the top 10 most played songs?

### Q: What were the top 10 most popular artists by runtime?

We are unable to run these queries since there seems to be no overlap between activity log and songs and artists database. 
Hence we will ask a few questions that can be answered from this data

### Q: Who are the top 10 users by number of songs heard?

`SELECT p.user_id, u.first_name, u.last_name, COUNT(p.user_id) FROM songplays AS p JOIN users AS u ON u.user_id = p.user_id GROUP BY 1, 2, 3 ORDER BY 4 DESC LIMIT 10;`

user_id 	first_name 	last_name 	count
49 	Chloe 	Cuevas 	689
80 	Tegan 	Levine 	665
97 	Kate 	Harrell 	557
15 	Lily 	Koch 	463
44 	Aleena 	Kirby 	397
29 	Jacqueline 	Lynch 	346
24 	Layla 	Griffin 	321
73 	Jacob 	Klein 	289
88 	Mohammad 	Rodriguez 	270
36 	Matthew 	Jones 	248

