# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
user_history_table_drop = "DROP TABLE IF EXISTS user_history;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id SERIAL,
    start_time bigint NOT NULL, 
    user_id int NOT NULL, 
    song_id varchar(20), 
    artist_id varchar(20),
    session_id int NOT NULL, 
    level varchar, 
    location varchar, 
    user_agent varchar
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id int PRIMARY KEY,
    first_name varchar NOT NULL, 
    last_name varchar, 
    gender varchar, 
    level varchar DEFAULT 'free',
    start_time bigint
);
""")

user_history_table_create = ("""
CREATE TABLE IF NOT EXISTS user_history (
    user_id int,
    start_time bigint,
    level varchar DEFAULT 'free',
    PRIMARY KEY (user_id, start_time)
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id varchar(20) PRIMARY KEY, 
    title varchar NOT NULL, 
    artist_id varchar(20) NOT NULL, 
    year int, 
    duration float
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id varchar(20) PRIMARY KEY,
    name varchar NOT NULL,
    location varchar,
    latitude float,
    longitude float
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time bigint PRIMARY KEY,
    hour int, 
    day int, 
    week int, 
    month int, 
    year int, 
    weekday int
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, song_id, artist_id, session_id, level, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level, start_time)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (user_id)
DO UPDATE SET level = EXCLUDED.level WHERE EXCLUDED.start_time > users.start_time;
""")

user_history_table_insert = ("""
INSERT INTO user_history (user_id, start_time, level)
VALUES (%s, %s, %s);
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s);
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id, s.artist_id FROM songs AS s
JOIN artists AS a ON s.artist_id = a.artist_id
WHERE s.title = %s AND a.name = %s AND s.duration = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, user_history_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, user_history_table_drop, song_table_drop, artist_table_drop, time_table_drop]