import mysql.connector as mysql
import csv
# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')
from parse_ingredients import parse_ingredient
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] # must 'localhost' when running this script outside of Docker

with open('RecipeDatabase.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
data = data[1:]
ing_recs = []
for row in data:
  row.append("https://img.icons8.com/cute-clipart/64/000000/bookmark-ribbon.png")
  row[2] = str(row[2])
  row[9] = int(row[9])
  row[10] = int(row[10])
  row[8] = int(row[8])
  row[1] = int(row[1])
  row[7] = str(row[7])
  records = []
  ingredients = row[3].split(';')
  for i in ingredients:
    ing = parse_ingredient(i)
    records.append((str(row[0]),str(ing.name), 'unknown', ( " "+str(ing.quantity)), str(ing.unit), 3.14, ))
    
  ing_recs.append(records) 






with open('IngredientDatabase.csv', newline='') as csvfile:
  idata = list(csv.reader(csvfile))
  idata = idata[1:]
  for irow in idata:
    irow[0] = str(irow[0])


# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
try:
  cursor.execute("DROP TABLE IF EXISTS Users;")
  cursor.execute("DROP TABLE IF EXISTS Recipes;")
  cursor.execute("DROP TABLE IF EXISTS Bookmarks;")
  cursor.execute("DROP TABLE IF EXISTS Ingredients;")
  cursor.execute("DROP TABLE IF EXISTS Basket;")
  cursor.execute("DROP TABLE IF EXISTS ParsedIngredients;")
  db.commit()
except (mysql.Error, mysql.Warning) as e:
  print(e, 'ERROR')

# Create a TStudents table (wrapping it in a try-except is good practice)
try:
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
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
    CREATE TABLE IF NOT EXISTS Recipes (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      name        VARCHAR(100) NOT NULL,
      time        INT NOT NULL,
      serving     VARCHAR(100),
      ingredients VARCHAR(4000) NOT NULL,
      instructions VARCHAR(4000) NOT NULL,
      nutrition   VARCHAR(2000),
      related     VARCHAR(500),
      image        VARCHAR(1000) NOT NULL,
      
      taste       INT NOT NULL,
      ease        INT NOT NULL,
      cleanup     INT NOT NULL,
      bookmark    VARCHAR(500) NOT NULL,

      created_at  datetime default(current_timestamp)
    );
  """)
except (mysql.Error, mysql.Warning) as e:
  print(e, 'ERROR')


try:
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Bookmarks (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      email       VARCHAR(100),
      name        VARCHAR(100) NOT NULL,
      time        INT NOT NULL,
      serving     VARCHAR(100),
      ingredients VARCHAR(4000) NOT NULL,
      instructions VARCHAR(4000) NOT NULL,
      nutrition   VARCHAR(2000),
      related     VARCHAR(500),
      image        VARCHAR(1000) NOT NULL,
        taste       INT NOT NULL,
      ease        INT NOT NULL,
      cleanup     INT NOT NULL,
      bookmark VARCHAR(500) NOT NULL,
      created_at  datetime default(current_timestamp)
    );
  """)
except (mysql.Error, mysql.Warning) as e:
  print(e, 'ERROR')
  
try:
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ingredients (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      ingredient  VARCHAR(50) NOT NULL
    );
  """)
except:
  print("Ingredient table already exists. Not recreating it.")

try:
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Basket (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      ingredient  VARCHAR(200) NOT NULL,
      category VARCHAR(100)    NOT NULL,
      quantity varchar(100)      NOT NULL,
      unit varchar(100)        NOT NULL,
      cost float               NOT NULL,
      email VARCHAR(200)       NOT NULL
    );
  """)

  # example record:
  # ingredient: "cheddar cheese"
  # category: "dairy"
  # quantity: 8
  # unit: "oz"
  # cost: 4.35
  # email "user@gmail.com"

except:
  print("Basket table already exists. Not recreating it.")

try:
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS ParsedIngredients (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      recipe      VARCHAR(100)  not null,
      ingredient  VARCHAR(200) NOT NULL,
      category VARCHAR(100)    NOT NULL,
      quantity varchar(100)         NOT NULL,
      unit varchar(100)        NOT NULL,
      cost float               NOT NULL    
    );
  """)

  # example record:
  # ingredient: "cheddar cheese"
  # category: "dairy"
  # quantity: 8
  # unit: "oz"
  # cost: 4.35
  # email "user@gmail.com"

except:
  print("Basket table already exists. Not recreating it.")
  

# Insert Records
query = "insert into Users (full_name, email, password) values (%s, %s,  %s);"
values = [
  ('Andrew Hernandez','anh190@ucsd.edu', '54Soleda')
  
]

cursor.executemany(query, values)
query = """insert into Recipes (name, time, serving, ingredients, instructions,
            nutrition, related, image, taste, ease, cleanup, bookmark) values (%s, %s,  %s,%s, %s,  %s,%s, %s,  %s,%s, %s, %s);"""
cursor.executemany(query, data)

query = """insert into Ingredients (ingredient) values (%s);"""
cursor.executemany(query, idata)
db.commit()

for i in ing_recs:

  query = """insert into ParsedIngredients (recipe,ingredient, category, quantity, unit, cost) values (%s, %s, %s, %s, %s, %s);"""
  cursor.executemany(query, i)
  db.commit()

# Selecting Records
cursor.execute("select * from Users;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]

cursor.execute("select * from Recipes;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]

cursor.execute("select * from Ingredients;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]
db.close()
