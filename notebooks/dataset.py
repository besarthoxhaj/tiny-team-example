#%%
import torch
import torchvision
import psycopg2
import dotenv
import httpx
import pathlib
import PIL
import os
import io


dotenv.load_dotenv("/root/tiny-team-example/.env")
S3 = "https://tiny-images-jk9apq.s3.us-east-1.amazonaws.com/{KEY}.jpg"
QUERY = """
  WITH numbered_rows AS (
    SELECT
      item_key,
      label,
      ROW_NUMBER() OVER (PARTITION BY label ORDER BY item_key) AS rn
    FROM img_labels
    ORDER BY
      item_key
  )
  SELECT
    item_key,
    label
  FROM numbered_rows
  WHERE
    rn <= 100;
"""


#%%
class ImageDataset(torch.utils.data.Dataset):
  def __init__(self, params):
    self.conn = psycopg2.connect(**params)
    self.cursor = self.conn.cursor()
    self.image_cache_dir = pathlib.Path.home() / ".tiny_img_cache"
    self.transform = torchvision.transforms.Compose([
      torchvision.transforms.Resize(256),
      torchvision.transforms.CenterCrop(224),
      torchvision.transforms.ToTensor(),
      torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    self.item_keys, self.labels = self.load_data_from_database()
    self.label_dict = {label: i for i, label in enumerate(sorted(set(self.labels)))}
    self.labels = [self.label_dict[label] for label in self.labels]
    self.labels = torch.tensor(self.labels)

  def load_data_from_database(self):
    self.cursor.execute(QUERY)
    rows = self.cursor.fetchall()
    item_keys, labels = zip(*rows)
    return item_keys, labels

  def __len__(self):
    return len(self.item_keys)

  def __getitem__(self, index):
    item_key = self.item_keys[index]
    label = self.labels[index]
    image_path = os.path.join(self.image_cache_dir, f"{item_key}.jpg")

    if not os.path.exists(image_path):
      s3_url = S3.format(KEY=item_key)
      res = httpx.get(s3_url)
      os.makedirs(self.image_cache_dir, exist_ok=True)
      f = open(f"{self.image_cache_dir}/{item_key}.jpg", "wb")
      f.write(res.content)
      f.close()

    image = PIL.Image.open(image_path)
    image = self.transform(image)
    return image, label