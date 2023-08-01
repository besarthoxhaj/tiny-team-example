#%%
import matplotlib.pyplot as plt
import psycopg2
import numpy as np
import random
import dotenv
import httpx
import faiss
import PIL
import os
import io
#%%
S3 = "https://tiny-images-jk9apq.s3.us-east-1.amazonaws.com/{KEY}.jpg"
dotenv.load_dotenv("/root/tiny-team-example/.env")
USER = os.environ.get("POSTGRES_USER")
DATABASE = os.environ.get("POSTGRES_DB")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")
HOST = "localhost"
#%%
conn = psycopg2.connect(host=HOST, user=USER, password=PASSWORD, dbname=DATABASE)
cur = conn.cursor()
cur.execute("SELECT item_key, embedding FROM img_predictions ORDER BY RANDOM() LIMIT 1200;")
rows = cur.fetchall()
cur.close()
conn.close()
#%%
target_item_id = "item_key"
embeddings_dict = {}
embeddings_list = []
#%%
for row in rows:
  item_key, embedding = row
  embedding = np.array(embedding)
  embeddings_dict[item_key] = embedding
  embeddings_list.append(embedding)
#%%
embedding_dimension = len(embeddings_list[0])
index = faiss.IndexFlatL2(embedding_dimension)
print("index.is_trained", index.is_trained)
#%%
embeddings_array = np.array(embeddings_list).astype("float32")
print("embeddings_array.shape", embeddings_array.shape)
faiss.normalize_L2(embeddings_array)
index.add(embeddings_array)
#%% Target embedding example
item_keys = list(embeddings_dict.keys())
random_key = random.choice(item_keys)
target_embedding = (embeddings_dict[random_key]).reshape(1, -1).astype("float32")
faiss.normalize_L2(target_embedding)
#%%
distances, indices = index.search(target_embedding, 6)
print("indices", indices)
print("distances", distances)
#%%
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 12))
# Flattens the axes to one-dimensional, so
# we can iterate over it in a simple loop
axes = axes.flatten()

for i in range(indices.shape[1]):
  distance = distances[0, i]
  item_id = list(embeddings_dict.keys())[indices[0, i]]
  img_url = S3.format(KEY=item_id)
  response = httpx.get(img_url)
  image = PIL.Image.open(io.BytesIO(response.content))
  axes[i].set_title(f'Distance: {distance:.4f}')
  axes[i].imshow(image)
print("SHOW IMAGES")
plt.show()