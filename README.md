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
+ columns: `songplay_id, start_time, user_id, song_id, artist_id, session_id, level, location, user_agent`
+ primary key: `songplay_id` - serial datatype
+ non nullable: `start_time, user_id`

Every record should contain the time when it was played and who played it. Hence these two columns should be non nullable.
Ideally the song_id (and hence artist_id) should be non-nullable since these are also important information to know what was played. However in this sample dataset we will not have this information, hence we will allow nulls so that we can do some alternate queries on the database to show the value of a star schema in RDBMS.
It might also help to store the song name and title name for the records that weren't processed so that we could come back it to later on, however the song and artist data is expected to be processed completely at first, and only then the songplay log data will be processed. This will ensure that all songplays has an associated songid and artistid associated with it in the full dataset.

### Dimension Tables

#### artists
+ columns: `artist_id, name, location, latitude, longitude`
+ primary key: `artist_id` 
+ non nullable: `name`

It is expected that every artist has a name. Without this the information is not useful.

Artist information is retrieved from the song records. Since we have a single file for each song, it means that there will be a repetition of artists across multiple song files. In order to handle this, we will DO NOTHING when inserting duplicates into the artist table.

#### songs
+ columns: `song_id, title, artist_id, year, duration`
+ primary key: `song_id`
+ non nullable: `title, artist_id`

Every song should have a title and should be associated with an artist. This is the minimum expectation that is expected out of a clean dataset.
It is also important that the song should have a duration and year, but this is metatdata and we'll not check for nullness of this data. Recording this as-is will give us the ability to check for bad data at a later stage and rectify.

#### users
+ columns: `user_id, first_name, last_name, gender, level, start_time`
+ primary key: `user_id`
+ non nullable: `first_name`

At least the first name of the user should be available for data sanity reasons.
We will also default the level to `free` in case the data was not found for any reason.
We will also store the start_time with every record so that we can update with only newer records when there is a change in level.

User records are retrieved from the logs. The users can be paid or free users. The user might have also changed their level status during a point of time. We'd like to store the record of what is the current level of the user in the users table. It would be good to also store the history of the users as an additional table in case we would like to known when a user changed their subscription.

#### time
+ columns: `start_time, hour, day, week, month, year, weekday`
+ primary key: `start_time`

We need to have just a single record for every unique timestamp. Hence we will mark the start timestamp as a primary key.

#### user_history
+ columns: `user_id, start_time, level`
+ primary key: `user_id, start_time`
+ non nullable: `start_time`

This is an additional table that we are creating to record the history of users changing their subscription levels.

**Note:** Currently a history record is being inserted whenever a new timestamp for the same user is found in a new file. This can be fixed by inserting a new record only when the level changes across log files. This is an improvement that can be taken up for later.

## Project Files

### Python Scripts
#### sql_queries.py
This contains the actual SQL queries to create, drop, insert and select from tables. 

#### create_table.py
This file has to be run first always before any session so that the existing tables are dropped and new clean tables are created.

#### etl.py
This contains the ETL pipeline to read from all the json files, process them, and finally insert the records into the created tables.
When this file is run, all the data is populated into the database.

### Jupyter Notebooks
#### test.ipynb
This notebook contains a few test and debugging queries that can be used to check that the SQL statements are fine and the ETL pipeline is working fine

#### etl.ipynb
This notebook is the exploratory workbook that is used to analyse the data files and build out a sample ETL pipeline. Once we are happy with this, we can move the logic into a python script.

#### analysis.ipynb
Once all the data is inserted into the tables, we can use this notebook to run some sample queries and analysis.


## Data Analysis - sample questions

### Q: What were the top 10 most played songs?

### Q: What were the top 10 most popular artists by runtime?

We are unable to run these queries since there seems to be no overlap between activity log and songs and artists database. 
Hence we will ask a few questions that can be answered from this data

### Q: Who are the top 10 users by number of songs heard?

`SELECT p.user_id, u.first_name, u.last_name, COUNT(p.user_id) FROM songplays AS p JOIN users AS u ON u.user_id = p.user_id GROUP BY 1, 2, 3 ORDER BY 4 DESC LIMIT 10;`

| user_id | first_name | last_name | count |
|---------|------------|-----------|-------|
|49 | Chloe | Cuevas | 689 |
|80 | Tegan | Levine | 665 |
|97 | Kate | Harrell | 557 | 
|15 | Lily | Koch | 463 |
|44 | Aleena | Kirby | 397 |
|29 | Jacqueline | Lynch | 346 |
|24 | Layla | Griffin | 321 |
|73 | Jacob | Klein | 289 |
|88 | Mohammad | Rodriguez | 270 |
|36 | Matthew | Jones | 248 |

