import confluent_kafka
import prometheus_client
import psycopg2
import json
import utils


utils.check_connection_status("postgres", 5432)
p = psycopg2.connect(host="postgres", user="root", port=5432, database="W9sV6cL2dX", password="E5rG7tY3fH")
k = confluent_kafka.Consumer({"bootstrap.servers": "kafka:29092", "group.id": "logs-group-1", "auto.offset.reset": "earliest"})
k.subscribe(["logs"])


PG_INSERTS = prometheus_client.Counter("pg_inserts", "Postgres Inserts")
PG_ERRORS = prometheus_client.Counter("pg_errors", "Postgres Errors")


def insert_to_postgres(cur_res):
  user_id = str(cur_res["user_id"])
  print("user_id", user_id)


def main():
  while True:
    msg = k.poll(1.0)
    if msg is None: continue
    if msg.error(): continue
    raw_res = msg.value().decode("utf-8")
    cur_res = json.loads(raw_res)
    insert_to_postgres(cur_res)


if __name__ == "__main__":
  prometheus_client.start_http_server(9965)
  main()