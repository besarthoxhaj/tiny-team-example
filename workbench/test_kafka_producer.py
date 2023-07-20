#%%
import confluent_kafka
import json
import uuid
import random
import time
#%%
config = {'bootstrap.servers': 'localhost:29092'}
producer = confluent_kafka.Producer(config)
#%%
while True:
  topic = f"test-topic-{random.randint(0, 9)}"
  item_id = str(uuid.uuid4())
  session = str(uuid.uuid4())
  user_id = random.randrange(0, 5000)
  ts = int(time.time())

  log_msg = json.dumps({"type": "reco", "user_id": random.randrange(0, 5000), "session": session, "item_id": item_id, "ts": ts})
  producer.produce(topic, log_msg)
  print("flush to topic:", topic)
  producer.flush()
  time.sleep(5)
# %%
