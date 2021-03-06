import os
import glob
import psycopg2
import pandas as pd
import numpy as np
from sql_queries import *


def process_song_file(cur, filepath):
    """ Extracts the song and artist information from the json file and inserts into the database
    
    Args:
    cur: the cursor to the database
    filepath: the path to the json file that contains the song data
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df.loc[:, ['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    try:
        cur.execute(song_table_insert, song_data)
    except psycopg2.Error as e:
        print('Error inserting song: ', song_data)
        print(e)
    
    # insert artist record
    artist_data = df.loc[:, ['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    try:
        cur.execute(artist_table_insert, artist_data)
    except psycopg2.Error as e:
        print('Error inserting artist: ', artist_data)
        print(e)


def process_log_file(cur, filepath):
    """ Extracts the time, user and songplay information from the json file and inserts into the database
    
    Args:
    cur: the cursor to the datbase
    filepath: the path to the json file containing songplay records
    """
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.query('page == "NextSong"')

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'])
    
    # insert time data records
    time_data = (t.values, t.dt.hour.values, t.dt.day.values, t.dt.weekofyear.values, t.dt.month.values, t.dt.year.values, t.dt.weekday.values)
    column_labels = ('timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(data={l: d.tolist() for l, d in zip(column_labels, time_data)})

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.loc[:, ['userId', 'firstName', 'lastName', 'gender', 'level', 'ts']]
    user_df = user_df.drop_duplicates(subset=['userId', 'level']) # drop any duplicates # drop any duplicates

    # insert user records
    try:
        for i, row in user_df.iterrows():
            cur.execute(user_table_insert, row)
    except psycopg2.Error as e:
        print('Error inserting user: ', row)
        print(e)

    # insert user history records
    try:
        for i, row in user_df.iterrows():
            cur.execute(user_history_table_insert, (row[0], row[5], row[4]))
    except psycopg2.Error as e:
        print('Error insert user history: ', row)
        print(e)
        
    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
#         print((row.song, row.artist, row.length), results)
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, songid, artistid, row.sessionId, row.level, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """ Processes all the files within the given directory for insertion into database
    
    This function will walk through the specified path and retrieve all the files that
    are present in the directory tree. It will then call the specified callback function 
    for every json file that is found in the directory tree.
    
    Args:
    cur: the cursor to the database
    conn: the database connection to be used
    filepath: the root folder that contains all the necessary files to be processed
    func: the callback function that will process the retrieved files
    
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """ The main function that is called when the program starts
    """
    
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()