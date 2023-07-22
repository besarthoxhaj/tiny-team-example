import psycopg2
import httpx


connection = psycopg2.connect(host="localhost", user="root", port=5432, database="W9sV6cL2dX", password="E5rG7tY3fH")
connection.autocommit = True
cursor = connection.cursor()


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