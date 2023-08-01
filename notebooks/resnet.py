#%%
import torch
import random
import numpy
import dataset
import wandb
import utils
import json
import os
#%%
torch.manual_seed(42)
numpy.random.seed(42)
random.seed(42)
gen = torch.Generator().manual_seed(42)
#%%
def seed_worker(worker_id):
  worker_seed = torch.initial_seed() % 2**32 + worker_id
  numpy.random.seed(worker_seed)
  random.seed(worker_seed)
#%%
USER = os.environ.get("POSTGRES_USER")
DATABASE = os.environ.get("POSTGRES_DB")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")
params = { "host": "localhost", "user": USER, "port": 5432, "database": DATABASE, "password": PASSWORD }
#%%
ds = dataset.ImageDataset(params)
reverse_label_dict = {value: key for key, value in ds.label_dict.items()}
with open('class_map.json', 'w') as fp: json.dump(reverse_label_dict, fp)
trn_len = int(0.8 * len(ds))
tst_len = len(ds) - trn_len
trn_ds, tst_ds = torch.utils.data.random_split(ds, [trn_len, tst_len], generator=gen)
trn_dl = torch.utils.data.DataLoader(trn_ds, batch_size=8, shuffle=True, num_workers=4, worker_init_fn=seed_worker, generator=gen)
tst_dl = torch.utils.data.DataLoader(tst_ds, batch_size=8, shuffle=True, num_workers=4, worker_init_fn=seed_worker, generator=gen)
#%%
class CustomResNet(torch.nn.Module):
  def __init__(self, num_classes):
    super(CustomResNet, self).__init__()
    self.resnet = torch.hub.load("pytorch/vision:v0.10.0", "resnet18", weights="ResNet18_Weights.IMAGENET1K_V1")
    self.resnet.fc = torch.nn.Linear(512, 256, bias=True)
    self.relu = torch.nn.ReLU()
    self.last = torch.nn.Linear(256, num_classes, bias=True)

  def forward(self, x):
    x = self.resnet(x)
    x = self.relu(x)
    emb = x # save embeddings
    x = self.last(x)
    return x, emb
#%%
model = CustomResNet(24)
for param in model.parameters(): param.requires_grad = False
for param in model.resnet.fc.parameters(): param.requires_grad = True
for param in model.last.parameters(): param.requires_grad = True
#%%
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(list(model.resnet.fc.parameters()) + list(model.last.parameters()), lr=0.001)
#%%
config = { "learning_rate": 0.001, "architecture": "resnet18", "epochs": 2 }
wandb.init(project="tiny-imgs-classification", config=config)
#%%
for epoch in range(3):
  model.train()
  trn_loss = 0.0
  trn_acc  = 0.0
  for i, (x, y) in enumerate(trn_dl):
    # utils.show_batch_images(x, y.tolist(), reverse_label_dict)
    optimizer.zero_grad()
    output, emb = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    trn_loss += loss.item()
    trn_acc  += utils.accuracy(output, y)

    if (i % 50 == 0) and (i > 0):
      val_loss = 0.0
      val_acc  = 0.0
      with torch.no_grad():
        model.eval()
        for _, (x, y) in enumerate(tst_dl):
          output, emb = model(x)
          loss = criterion(output, y)
          val_loss += criterion(output, y).item()
          val_acc  += utils.accuracy(output, y)
      val_loss /= len(tst_dl)
      val_acc  /= len(tst_dl)
      trn_loss /= 50
      trn_acc  /= 50
      wandb.log({"val_acc": val_acc, "val_loss": val_loss, "trn_acc": trn_acc, "trn_loss": trn_loss})
      print(f"Epoch {epoch} | Batch {i:4} | trn_loss {trn_loss:.4f} | trn_acc {trn_acc:.4f} | val_loss {val_loss:.4f} | val_acc {val_acc:.4f}")


#%%
torch.save(model.state_dict(), "/root/tiny-team-example/weights/00.pth")
