# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = (""" 
    CREATE TABLE IF NOT EXISTS songplays(
        songplay_id SERIAL PRIMARY KEY,
        start_time TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        level VARCHAR NOT NULL, 
        song_id VARCHAR,
        artist_id VARCHAR,
        session_id INT NOT NULL,
        location VARCHAR NOT NULL,
        user_agent VARCHAR NOT NULL,
        CONSTRAINT fk_time
            FOREIGN KEY(start_time)
                REFERENCES time(start_time)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        CONSTRAINT fk_users
            FOREIGN KEY(user_id)
                REFERENCES users(user_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        CONSTRAINT fk_songs
            FOREIGN KEY(song_id)
                REFERENCES songs(song_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        CONSTRAINT fk_artists
            FOREIGN KEY(artist_id)
                REFERENCES artists(artist_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT PRIMARY KEY,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        gender VARCHAR NOT NULL,
        level VARCHAR NOT NULL
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id VARCHAR PRIMARY KEY,
        title VARCHAR NOT NULL,
        artist_id VARCHAR NOT NULL,
        year INT,
        duration NUMERIC
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR PRIMARY KEY,
        name VARCHAR NOT NULL,
        location VARCHAR,
        latitude NUMERIC,
        longitude NUMERIC
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP PRIMARY KEY,
        hour INT NOT NULL,
        day INT NOT NULL,
        week INT NOT NULL,
        month INT NOT NULL,
        year INT NOT NULL,
        weekday INT NOT NULL
    );
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT(songplay_id)
    DO NOTHING;
""")

user_table_insert = ("""
    INSERT INTO users
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT(user_id)
    DO UPDATE
        SET first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            gender = EXCLUDED.gender,
            level = EXCLUDED.level;
""")

song_table_insert = ("""
    INSERT INTO songs
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT(song_id)
    DO NOTHING;
""")

artist_table_insert = ("""
    INSERT INTO artists
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT(artist_id)
    DO NOTHING;
""")


time_table_insert = ("""
    INSERT INTO time
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT(start_time)
    DO NOTHING;
""")

# FIND SONGS

song_select = ("""
    SELECT song_id, artist_id FROM songs
    JOIN artists
    USING(artist_id)
    where title = %s AND name = %s AND duration = %s;
""")

# QUERY LISTS


# create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
# I changed the order of create table queries becuase songplay_create_table needed user_table, song_table, etc. to be created first, foreign key constraint.
create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]