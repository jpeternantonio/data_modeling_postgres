import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    
    The function reads song data which is in a JSON format and transfers the data to a list.
    The transfered data will be cleaned and will remove the duplicates in the process. After that, 
    the data will insert to a designated table.
    
        Parameters:
            cur (func): the cursor object(executes sql statements).
            filepath (str): song data file path

        Returns:
            None
        
    """
    
    df = pd.read_json(filepath, lines=True)
    songs_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].copy()
    
    songs_data.dropna(subset=['title'], inplace=True)
    songs_data.drop_duplicates(subset=['title'], inplace=True)
    
    for i, song_data in songs_data.iterrows():
        cur.execute(song_table_insert, song_data)
    
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 
                  'artist_longitude']].copy()
    
    artist_data.dropna(subset=['artist_name'], inplace=True)
    artist_data.drop_duplicates(subset=['artist_name'], inplace=True)
    
    for i, row in artist_data.iterrows():
        cur.execute(artist_table_insert, row)


def process_log_file(cur, filepath):
    """
    
    This function reads the log data which is in a JSON format and transfers the data to a list. 
    The transfered data will be filtered, converted, cleaned, and will remove the duplicates in the process. After that, 
    the data will be inserted to a designated table.
    
        Parameters:
            cur (func): the cursor object(executes sql statements).
            filepath (str): log data file path

        Returns:
            None
            
    """
   
    df = pd.read_json(filepath, lines=True) 
    df = df.loc[df['page'] == 'NextSong']
    
    t = pd.to_datetime(df['ts'], unit='ms')
    time_data = [t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ['timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_data_dict = {column_name: data_series for data_series, column_name in zip(time_data, column_labels)}
    time_df = pd.DataFrame(time_data_dict)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].copy()
    user_df.dropna(subset=['userId'], inplace=True)
    user_df.drop_duplicates(subset=['userId'], inplace=True) 

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    for index, row in df.iterrows():
        start_time = pd.to_datetime(row['ts'], unit='ms')
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        songplay_data = (start_time, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    The function retrieves JSON files from a directory or filepath and transforms the data to
    insert it into the database. It will also show or print in the terminal the file/s 
    found and processed.
    
        Parameters:
        cur (func): cursor object(executes sql commands)
        conn (func): object that connects to the database
        filepath (str): log data and song data directories
        func (func): function that transforms the files and inserts it into the database

        Returns: 
            None
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    
    This establishes a connection to the database, execute process_data and
    close the connection to database.
    
        Returns:
            None
    
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()