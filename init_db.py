import mysql.connector as mysql
import csv
# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] # must 'localhost' when running this script outside of Docker

with open('Recipe Database.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
data = data[1:]
for row in data:
  row[2] = str(row[2])
  row[9] = int(row[9])
  row[10] = int(row[10])
  row[8] = int(row[8])
  row[1] = int(row[1])
  row[7] = str(row[7])




# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
try:
  cursor.execute("DROP TABLE IF EXISTS Users;")
  cursor.execute("DROP TABLE IF EXISTS Recipes;")
  db.commit()
except (mysql.Error, mysql.Warning) as e:
  print(e, 'ERROR')

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

try:
  cursor.execute("""
    CREATE TABLE Recipes (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      name        VARCHAR(100) NOT NULL,
      time        INT NOT NULL,
      serving     VARCHAR(100),
      ingredients VARCHAR(5000) NOT NULL,
      instructions VARCHAR(10000) NOT NULL,
      nutrition   VARCHAR(5000),
      related     VARCHAR(5000),
      image        VARCHAR(1000) NOT NULL,
        taste       INT NOT NULL,
      ease        INT NOT NULL,
      cleanup     INT NOT NULL,
      created_at  datetime default(current_timestamp)
    );
  """)
except :
  print( 'ERROR')
  

# Insert Records
query = "insert into Users (full_name, email, password) values (%s, %s,  %s);"
values = [
  ('Andrew Hernandez','anh190@ucsd.edu', '54Soleda')
  
]

cursor.executemany(query, values)
query = """insert into Recipes (name, time, serving, ingredients, instructions,
            nutrition, related, image, taste, ease, cleanup) values (%s, %s,  %s,%s, %s,  %s,%s, %s,  %s,%s, %s);"""
cursor.executemany(query, data)
db.commit()

# Selecting Records
cursor.execute("select * from Users;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]

cursor.execute("select * from Recipes;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]
db.close()
