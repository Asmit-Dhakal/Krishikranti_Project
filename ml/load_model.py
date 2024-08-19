import torch
from .models import ResNet9  # Make sure this path matches your model's location


def load_model():
    model = ResNet9(in_channels=3, num_classes=10)
    model.load_state_dict(torch.load('./deepmodel/model.pth', map_location=torch.device('cpu'),weights_only=True))
    model.eval()  # Set the model to evaluation mode
    return model


model = load_model()