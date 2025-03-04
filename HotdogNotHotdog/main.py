import torch
import torchvision.transforms as transforms
from torchvision import datasets
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torch import nn
import torchvision.transforms.functional as TF
from PIL import Image
import matplotlib.pyplot as plt
import os





hotdogPhotosPath = os.path.join(os.path.dirname(__file__), r"classes\\hotdog")   # Path to the folder with hotdogs
notHotdogPhotosPath = os.path.join(os.path.dirname(__file__), r"classes\\nothotdog")   # Path to the folder with nothotdogs
classesFolder = os.path.join(os.path.dirname(__file__), "classes")   # Path to the folder with classes


# Walk through the hotdogs and nothotdogs and save all images as JPEG
def saveAsJPEG(photosPath: str) -> None:
    for root, dirs, files in os.walk(photosPath):
        for file in files:
            if file.lower().endswith('.jfif'):  # Check for JFIF files
                file_path = os.path.join(root, file)
                img = Image.open(file_path)
                img = img.convert('RGB')  # Convert to RGB format
                new_file_path = file_path.replace('.jfif', '.jpg')
                img.save(new_file_path, 'JPEG')  # Save as JPEG


# Make all images 224 by 224 and filled with padding if necessary
def pad_to_square(image):
    width, height = image.size
    padding = (0, 0, 0, 0)
    if width != height:
        diff = abs(width - height)
        if width > height:
            padding = (0, diff // 2, 0, diff - diff // 2)
        else:
            padding = (diff // 2, 0, diff - diff // 2, 0)

    return TF.pad(image, padding, fill=0, padding_mode='constant')

transform = transforms.Compose([
    transforms.Lambda(pad_to_square),
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])


# Load your hotdog dataset
hotdog_dataset = datasets.ImageFolder(root=classesFolder, transform=transform)

print(hotdog_dataset.class_to_idx)  
# This prints out: {'hotdog': 0, 'nothotdog': 1}


class hotdogLinearModel(nn.Module):
    def __init__(self, inputShape : int, hiddenUnits: int, outputShape: int):
        super().__init__()
        self.layerStack = nn.Sequential(
            nn.Flatten(),   # Flattens input if it's an image (needed if input is not already a vector)
            nn.Linear(in_features=inputShape, out_features=hiddenUnits),
            nn.ReLU(),    # Activation function for better learning
            nn.Linear(in_features=hiddenUnits, out_features=outputShape),
            nn.Sigmoid()    # Ensures output is between 0 and 1 for binary classification
        )
    def forward(self, x):
        #print(self.layerStack(x))
        return self.layerStack(x)
    def predict(self, imagePath): 
        # Set model to evaluation mode
        self.eval()
        # Load the image
        # If imageInput is already a PIL Image, use it directly; otherwise, open it.
        if isinstance(imagePath, Image.Image):
            image = imagePath.convert("RGB")
        else:
            image = Image.open(imagePath).convert("RGB")
        # Ensure transformations match those used in training
        transformed_image = transform(image).unsqueeze(0)  # Add batch dimension

        # Move image to the same device as model
        device = next(self.parameters()).device
        transformed_image = transformed_image.to(device)

        # Make prediction
        with torch.no_grad():
            output = self.forward(transformed_image)
            
            # Apply sigmoid activation for binary classification
            confidence = torch.sigmoid(output).item()

            # Determine label (assuming hotdog = 0, not hotdog = 1)
            labelPrediction = "not hotdog" if confidence >= 0.50 else "hotdog"                     ###########################################################

            # Format confidence
            confidencePercentage = f"{confidence * 100:.2f}%"
            confidenceList = [{labelPrediction: confidencePercentage}]

        print(f'Prediction: {labelPrediction}\nConfidence: {confidenceList}')
        return labelPrediction, confidenceList



if __name__ == '__main__':

    def accuracy_fn(y_true, y_pred):
        y_pred_labels = (y_pred > 0.5).float()
        return (y_pred_labels.squeeze() == y_true.float()).float().mean().item()

    # Training step: one full pass over the training data
    def trainStep(model, optimizer, dataloader, lossFn):
        model.train()
        total_loss, total_acc = 0, 0

        for X, y in dataloader:
            optimizer.zero_grad()

            # Forward pass
            y_pred = model(X)
            # Ensure y has the same shape as y_pred by adding a dimension
            loss = lossFn(y_pred, y.unsqueeze(1).float())
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            total_acc += accuracy_fn(y, y_pred)

        return total_loss / len(dataloader), total_acc / len(dataloader)






    # Hyperparameters
    epochs = 30
    batch_size = 32
    learning_rate = 0.001



    # Create a DataLoader for the entire dataset
    train_loader = DataLoader(hotdog_dataset, batch_size=batch_size, shuffle=True)

    # Initialize the model (for binary classification, the model should output a single logit)
    model = hotdogLinearModel(inputShape=224*224*3, hiddenUnits=32, outputShape=1)

    # Setup optimizer and loss function (using BCELoss for binary classification)
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    lossFn = nn.BCELoss()

    # Training loop for the entire dataset
    for epoch in range(epochs):
        train_loss, train_acc = trainStep(model, optimizer, train_loader, lossFn)
        print(f"Epoch {epoch + 1}/{epochs} - Train loss: {train_loss:.5f}, Train acc: {train_acc:.5f}")












#    print("--------------------------------------------\n\n\n")
#    hotdog = r"fewfwfwefwefwf - Copy.jpg"
#    HPred1, HConf1 = model.predict(hotdog)

    # Open and display the image
#    image = Image.open(hotdog).convert("RGB")
#    plt.imshow(image)
#    plt.title(f"Prediction: {HPred1}")
#    plt.axis("off")
#    plt.show()


    torch.save(model.state_dict(), f'hotdogModel.pt')