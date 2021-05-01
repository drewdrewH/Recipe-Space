import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] # must 'localhost' when running this script outside of Docker

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
cursor.execute("drop table if exists Users;")

# Create a TStudents table (wrapping it in a try-except is good practice)
try:
  cursor.execute("""
    CREATE TABLE Users (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      full_name  VARCHAR(50) NOT NULL,
      email       VARCHAR(50) NOT NULL,
      password    VARCHAR(20) NOT NULL,
      created_at  datetime default(current_timestamp)
    );
  """)
except:
  print("Users table already exists. Not recreating it.")

# Insert Records
query = "insert into Users (full_name, email, password) values (%s, %s,  %s);"
values = [
  ('Andrew Hernandez','anh190@ucsd.edu', '54Soleda')
  
]
cursor.executemany(query, values)
db.commit()

# Selecting Records
cursor.execute("select * from Users;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]
db.close()
