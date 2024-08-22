import torch
from .models import mymodel  # Make sure this path matches your model's location


def load_model():
    model = mymodel(in_channels=3, num_classes=6)
    model.load_state_dict(torch.load('./deepmodel/riceleaf.pth', map_location=torch.device('cpu'),weights_only=True))
    model.eval()  # Set the model to evaluation mode
    return model


model = load_model()
