#%%
import os
import pandas
import dotenv
import psycopg2
#%%
dotenv.load_dotenv("/root/tiny-team-example/.env")
#%%
rootdir = "/root/tiny-team-example/training_data"
images = []
labels = []
#%%
for subdir, dirs, files in os.walk(rootdir):
  for file in files:
    # Only include .jpg files
    if file.endswith(".jpg"):
      # Extract the label from the subdir and file name from file
      label = os.path.basename(subdir)
      image_id = file.split(".")[0] # .jpg
      images.append(image_id)
      labels.append(label)
#%%
df = pandas.DataFrame({"id": images, "label": labels})
df.to_csv("/root/tiny-team-example/training_data/output.csv", index=False)
#%%
label_counts = df["label"].value_counts()
ax = label_counts.plot(kind="bar", figsize=(10, 6))
ax.set_title("Label Distribution")
ax.set_xlabel("Labels")
ax.set_ylabel("Count")
# %%
USER = os.environ.get("POSTGRES_USER")
DATABASE = os.environ.get("POSTGRES_DB")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")
c = psycopg2.connect(host="localhost", user=USER, port=5432, database=DATABASE, password=PASSWORD)
c.autocommit = True
cursor = c.cursor()
# %%
cursor.execute("""
  BEGIN;

  CREATE TABLE IF NOT EXISTS img_labels (
    item_key   UUID        PRIMARY KEY,
    label      VARCHAR(20) NOT NULL
  );

  COMMIT;
""")
# %%
for index, row in df.iterrows():
  cursor.execute("""
    INSERT INTO img_labels (item_key, label)
    VALUES (%s, %s);
  """, (row["id"], row["label"]))
# %%
cursor.execute("SELECT * FROM img_labels LIMIT 5;")
labels = cursor.fetchmany(10)
print("labels", labels)