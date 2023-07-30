import psycopg2
import httpx
import os


USER = os.environ.get("POSTGRES_USER")
DATABASE = os.environ.get("POSTGRES_DB")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")


connection = psycopg2.connect(host="localhost", user=USER, port=5432, database=DATABASE, password=PASSWORD)
connection.autocommit = True
cursor = connection.cursor()


insert_query = "INSERT INTO items (item_key, created_at, user_id, bucket_key, type) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (item_key) DO NOTHING;"
base_path = "http://135.181.118.171:7070/items/"
offset = 0


while True:
  print("Start offset:", offset)
  curr_url = base_path + str(offset)
  items = httpx.get(curr_url).json()
  if (len(items)) == 0: break

  insert_data = []
  for item in items: insert_data.append((
    item["item_key"],
    item["created_at"],
    item["user_id"],
    item["bucket_key"],
    item["type"],
  ))

  cursor.executemany(insert_query, insert_data)
  print("Finish offset:", offset)
  offset += 20000
