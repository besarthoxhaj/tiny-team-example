import confluent_kafka
import prometheus_client
import psycopg2
import datetime
import json
import utils


utils.check_connection_status("postgres", 5432)
p = psycopg2.connect(host="postgres", user="root", port=5432, database="W9sV6cL2dX", password="E5rG7tY3fH")
k = confluent_kafka.Consumer({"bootstrap.servers": "kafka:29092", "group.id": "logs-group-1", "auto.offset.reset": "earliest"})
k.subscribe(["logs"])
p.autocommit = True


PG_INSERTS = prometheus_client.Counter("pg_inserts", "Postgres Inserts")
PG_ERRORS = prometheus_client.Counter("pg_errors", "Postgres Errors")


def insert_to_postgres(store):

  insert_query = """
    INSERT INTO fct_hourly_metric (
      date_stamp,
      time_stamp,
      evnt_stamp,
      user_id,
      session_id,
      evt_type,
      item_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
  """

  insert_data = []

  for evt_log in store:
    cur_date = datetime.datetime.fromtimestamp(evt_log["ts"])

    insert_data.append((
      cur_date.date(),
      cur_date.replace(minute=0, second=0, microsecond=0),
      evt_log.get("ts"),
      evt_log.get("user_id"),
      evt_log.get("session"),
      evt_log.get("type"),
      evt_log.get("item_id")
    ))

  try:
    cursor = p.cursor()
    cursor.executemany(insert_query, insert_data)
    PG_INSERTS.inc(len(insert_data))
  except Exception as e:
    PG_ERRORS.inc()
    print("Worker error", e)


def main():
  store = []
  while True:
    msg = k.poll(1.0)
    if msg is None: continue
    if msg.error(): continue
    raw_res = msg.value().decode("utf-8")
    cur_res = json.loads(raw_res)
    store.append(cur_res)
    if len(store) > 5:
      insert_to_postgres(store)
      store = []


if __name__ == "__main__":
  prometheus_client.start_http_server(9965)
  main()