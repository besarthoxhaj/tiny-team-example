import torch
import matplotlib.pyplot as plt


def show_batch_images(tensor, labels, label_dict):
  tensor = tensor.permute(0,2,3,1) # adjust dimensions to [batch_size, width, height, channels]
  tensor = tensor.numpy() # convert tensor to numpy array
  n_images = tensor.shape[0]
  fig, axes = plt.subplots(1, n_images, figsize=(n_images*5, 5))
  for i, ax in enumerate(axes):
    ax.imshow(tensor[i])
    ax.set_title(label_dict[labels[i]])
    ax.axis('off')

  plt.show()


def accuracy(output, target):
  with torch.no_grad():
    pred = torch.argmax(output, dim=1)
    correct = pred.eq(target)
    acc = correct.float().mean().item()
    return acc