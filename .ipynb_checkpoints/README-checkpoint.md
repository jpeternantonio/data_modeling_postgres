# The Sparkify ETL Postgres Pipeline

## Project Overview
   A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app.
As a data engineer, we will create an ETL pipeline using Python that will extract song, artist, user, and log data from JSON files and load
the data into their Postgresql database. Once the process is finished, Sparkify data analyst will be able to explore the data and make an analysis
how the users interact with the app, what songs and artist the users listen to.

<br>

## Project Files
- data/
- sql_queries.py
- create_tables.py
- test.ipynb
- etl.ipynb
- etl.py


**data/** - This directory contains two folders. 'log_data/2018/11' which contains JSON files for user songplay log data.
'song_data/' which contains JSON files for song and artist data. These will be used for our database.

**sql_queries.py** - Python script file that contains SQL commands used to CREATE and DROP table, and INSERT values into our data tables. 

**create_tables.py** - Python file that have script for connecting to our POSTGRES database. This will also serve as a function
in executing 'sql_queries.py'.

**test.ipynb** - This Jupyter notebook contains SQL commands for testing or checking the created tables after executing 'create_tables.py' and
checking of table data after executing 'etl.ipynb' or 'etl.py'.

**etl.ipynb** - Jupyter notebook that contains Python scripts for extracting and transforming the data from JSON files and load it to our database.
This is also used for testing before executing the 'etl.py'.

**etl.py** - Python file that have same function of 'etl.ipynb'. Details of execution of these files was described below.

<br>

## Database Schema

The database consists of five tables arrannged in Star Schema. Check the image below:

<img src="sparkify_schema.png" alt="Database Schema" width="800"/>

The fact table is the 'songplays' table. It references the four dimension tables:
- 'songs'
- 'artists'
- 'users'
- 'time'

The schema is in 3rd Normal Form. Every table contains attributes that decribe the table itself. Primary key
and Foreign key are well defined in the figure to show table relation.

<br>

## Running The Scripts

In order to run the scripts locally, make sure you have postgresql in your machine.

[Install Postgresql](https://www.postgresql.org/download/)

Create a database with a name of 'studentdb' and user is 'student'.

Make sure you also installed Python3.6+ and Jupyter Notebook.

[Install Python](https://www.python.org/downloads/)

[Install Jupyter Notebook](https://jupyter.org/install)

Once you completed the steps above, you can run the following in your terminal:

'python create_tables.py'

If no errors, then run:

'python etl.py'

For checking, open the 'test.ipynb' using Jupyter Notebook and run all the cells to check the data tables.




