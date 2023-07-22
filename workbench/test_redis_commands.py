import redis


r = redis.Redis(host="localhost", port=6379, db=1, password="MvY4bQ7uN3", decode_responses=True)
random_key = r.randomkey()
random_item = r.hgetall(random_key)
print("random_item['id']", random_item['id'])