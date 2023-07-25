# Before using this make sure you have installed
# miniconda and created an environment with the
# packages: pytorch, torchvision
#
# Resources:
# - https://pytorch.org/hub/research-models
# - https://pytorch.org/hub/pytorch_vision_alexnet
# - https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
# - https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html

#%%
import os
import torch
import torchvision
import urllib
import PIL
#%%
class CustomAlexNet(torch.nn.Module):
  def __init__(self):
    super(CustomAlexNet, self).__init__()
    self.alexnet = torch.hub.load("pytorch/vision:v0.10.0", "alexnet", weights="AlexNet_Weights.DEFAULT")

  def forward(self, x):
    x = self.alexnet.features(x)
    x = self.alexnet.avgpool(x)
    x = torch.flatten(x, 1)
    for i in range(6): x = self.alexnet.classifier[i](x)
    embeddings = x
    x = self.alexnet.classifier[6](x)
    return x, embeddings
#%%
model = CustomAlexNet()
model = model.eval()
#%%
script_dir = os.path.dirname(os.path.realpath(__file__))
img_path = os.path.join(script_dir, "e14c4b33-b1e5-42a4-920d-b1c10a5a5545.jpg")
url = "https://tiny-images-jk9apq.s3.us-east-1.amazonaws.com/e14c4b33-b1e5-42a4-920d-b1c10a5a5545.jpg"
try: urllib.URLopener().retrieve(url, img_path)
except: urllib.request.urlretrieve(url, img_path)
input_image = PIL.Image.open(img_path)
#%%
preprocess = torchvision.transforms.Compose([
  torchvision.transforms.Resize(256),
  torchvision.transforms.CenterCrop(224),
  torchvision.transforms.ToTensor(),
  torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
#%%
input_tensor = preprocess(input_image)
print("input_tensor.shape", input_tensor.shape)
input_batch = input_tensor.unsqueeze(0)
print("input_batch.shape", input_batch.shape)
#%%
with torch.no_grad(): output, embs = model(input_batch)
print("output.shape", output.shape)
print("embs.shape", embs.shape)
probabilities = torch.nn.functional.softmax(output[0], dim=0)
print("probabilities.shape", probabilities.shape)
#%%
top5_prob, top5_catid = torch.topk(probabilities, 5)
classes_file_path = os.path.join(script_dir, "imagenet_classes.txt")
with open(classes_file_path, "r") as f: categories = [s.strip() for s in f.readlines()]
for i in range(top5_prob.size(0)): print(categories[top5_catid[i]], top5_prob[i].item())