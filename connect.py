import psycopg2
import os

dbname = os.getenv("DBNAME", "testdb")
dbuser = os.getenv("DBUSER", "postgres")
dbpass = os.getenv("PASSWORD", "root123")
dbhost = os.getenv("DBHOST", "localhost")
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL) 


