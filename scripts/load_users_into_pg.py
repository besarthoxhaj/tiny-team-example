import psycopg2
import httpx
import os


USER = os.environ.get("POSTGRES_USER")
DATABASE = os.environ.get("POSTGRES_DB")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")


connection = psycopg2.connect(host="localhost", user=USER, port=5432, database=DATABASE, password=PASSWORD)
connection.autocommit = True
cursor = connection.cursor()


print("Start")
insert_query = "INSERT INTO users (id, age, country, gender) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;"
base_path = "http://135.181.118.171:7070/users"
users = httpx.get(base_path).json()


insert_data = []
for user in users: insert_data.append((
  user["id"],
  user["age"],
  user["country"],
  user["gender"],
))


cursor.executemany(insert_query, insert_data)
cursor.close()
print("Finish")