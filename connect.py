import psycopg2
import os

DATABASE_URL = os.getenv('DATABASE_URL')

try:
    conn = psycopg2.connect(DATABASE_URL)

except:
    print "I am unable to connect to the database"
