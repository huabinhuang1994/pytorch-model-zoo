import torch
import torch.nn as nn
import torchvision.datasets as dsets
import torchvision.transforms as transforms
from torch.autograd import Variable
from model import ResidualBlock, ResNet

# Hyperparameters
lr = 0.001
epochs = 80
batch_size = 100

# Image Preprocessing
transform = transforms.Compose([
    transforms.Scale(40),
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32),
    transforms.ToTensor()])

# CIFAR-10 Dataset
train_dataset = dsets.CIFAR10(root='../datasets/',
                              train=True,
                              transform=transform,
                              download=True)

# Data Loader (Input Pipeline)
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size=batch_size,
                                           shuffle=True)

# Model
resnet = ResNet(block=ResidualBlock, layers=[2, 2, 2])
resnet = resnet.cuda()

# Loss and Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(resnet.parameters(), lr=lr)

# Training
for epoch in range(epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = images.cuda()
        labels = labels.cuda()
        images = Variable(images)
        labels = Variable(labels)

        # Forward + Backward + Optimize
        optimizer.zero_grad()
        outputs = resnet(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        if (i + 1) % batch_size == 0:
            print ("Epoch [%d/%d], Iter [%d/%d] Loss: %.4f" %
                   (epoch + 1, epochs, i + 1, len(train_loader), loss.data[0]))

    # Decaying Learning Rate
    if (epoch + 1) % 20 == 0:
        lr /= 3
        optimizer = torch.optim.Adam(resnet.parameters(), lr=lr)


# Save the Model
torch.save(resnet, '../trained/resnet.pkl')
