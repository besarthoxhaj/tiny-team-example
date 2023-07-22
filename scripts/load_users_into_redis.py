import psycopg2
import datetime
import redis


r = redis.Redis(host="localhost", port=6379, db=2, password="MvY4bQ7uN3")
connection = psycopg2.connect(host="localhost", user="root", port=5432, database="W9sV6cL2dX", password="E5rG7tY3fH")


with connection:
  cur = connection.cursor("sync_redis_cursor")
  cur.execute("SELECT id, age, gender, country FROM users;")
  batch_size = 5000
  curr_counter = 0

  while True:
    print("BATCH:", curr_counter)
    users = cur.fetchmany(batch_size)
    if not users: break
    curr_counter += 1
    pipe = r.pipeline()

    for user in users:
      id, age, gender, country = user
      item_key_redis = f"user:{id}"
      user_data = {"id": id, "age": age, "gender": gender, "country": country}
      filter_none = {k: v for k, v in user_data.items() if v is not None}
      pipe.hset(item_key_redis, mapping=filter_none)

    pipe.execute()
  cur.close()