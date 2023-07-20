#%%
import confluent_kafka
import json
#%%
consumer = confluent_kafka.Consumer({"bootstrap.servers": "localhost:29092", "group.id": "logs-group-1", "auto.offset.reset": "earliest"})
consumer.subscribe(["test-topic-7"])
#%%
while True:
    msg = consumer.poll(0.5)
    if msg is None: continue
    if msg.error(): continue
    raw_res = msg.value().decode("utf-8")
    cur_res = json.loads(raw_res)
    print("cur_res", cur_res)