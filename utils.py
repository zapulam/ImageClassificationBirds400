import os
import torch.nn as nn
import albumentations as A
import torchvision.models as models

from matplotlib import pyplot as plt


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def create_model(name, classes, pretrained):
    try:
        """
        Current models that can be used...
        alexnet, resnet18, squeezenet1_1, densenet121

        Add models here in a similar fashion...

        if name == "model"
            model = models.model()
            model.fc = nn.Linear(input, output)
        return model
        """

        if name == "alexnet":
            model = models.alexnet(pretrained=pretrained)
            model.classifier[6] = nn.Linear(4096, classes)
            return model

        elif name == "densenet121":
            model = models.densenet121(pretrained=pretrained)
            model.classifier = nn.Linear(1024, classes)
            return model

        elif name == "resnet18":
            model = models.resnet18(pretrained=pretrained)
            model.fc = nn.Linear(512, classes)
            return model

        elif name == "squeezenet1_1":
            model = models.squeezenet1_1(pretrained=pretrained)
            model.classifier._modules["1"] = nn.Conv2d(512, classes, kernel_size=(1, 1))
            model.num_classes = classes
            return model

        else:
            pass

    except:
        print("Model name not valid. Try again with valid model name. Models can be added in the create_model function of utils.py.")


def augment_image(image):
    transform = A.Compose([
            A.HorizontalFlip(p=0.5),
            A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=15, p=0.1),
            A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.1, brightness_by_max=True, p=0.1),        
            A.HueSaturationValue(hue_shift_limit=5, sat_shift_limit=5, val_shift_limit=5, p=0.1)
        ])
        
    augmented_image = transform(image=image)['image']
    return augmented_image


def create_plots(save_path, log):
    x = [item[0] for item in log]

    # Loss plot
    fig = plt.figure(figsize=(15,10))
    ax = fig.add_axes([0.1,0.1,0.75,0.75]) # axis starts at 0.1, 0.1
    ax.set_title("Loss per Epoch")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")

    tloss = [item[2] for item in log]
    vloss = [item[3] for item in log]

    ax.plot(x, tloss)
    ax.plot(x, vloss)

    ax.legend(['Training Loss', 'Validation Loss'])

    ax.set_ylim(ymax=7)
    ax.set_ylim(ymin=0)
    fig.savefig(os.path.join(save_path, 'loss.jpg'))
    plt.close(fig)

    # Accuracy plot
    fig = plt.figure(figsize=(15,10))
    ax = fig.add_axes([0.1,0.1,0.75,0.75]) # axis starts at 0.1, 0.1
    ax.set_title("Accuracy per Epoch")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Accuracy")

    train_acc_1 = [item[4] for item in log]
    train_acc_5 = [item[5] for item in log]
    valid_acc_1 = [item[6] for item in log]
    valid_acc_5 = [item[7] for item in log]

    ax.plot(x, train_acc_1)
    ax.plot(x, train_acc_5)
    ax.plot(x, valid_acc_1)
    ax.plot(x, valid_acc_5)

    ax.legend(['Train Acc@1', 'Train Acc@5', 'Valid Acc@1', 'Valid Acc@5'])

    ax.set_ylim(ymax=1)
    ax.set_ylim(ymin=0)
    fig.savefig(os.path.join(save_path, 'accuracy.jpg'))
    plt.close(fig)

"""
def create_plot(i, save_path, x, y, cols):
    fig = plt.figure(figsize=(15,10))
    ax = fig.add_axes([0.1,0.1,0.75,0.75]) # axis starts at 0.1, 0.1
    ax.set_title(cols[i] + " per Epoch")
    ax.set_xlabel("Epoch")
    ax.set_ylabel(cols[i])
    ax.plot(x, y)
    if i == 2 or i == 3:
        ax.set_ylim(ymax=7)
    else:
        ax.set_ylim(ymax=1)
    ax.set_ylim(ymin=0)
    fig.savefig(os.path.join(save_path, cols[i].lower().replace(" ", "_") + '.jpg'))
    plt.close(fig)
"""