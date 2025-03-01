import torch
import torchvision.transforms as transforms
from torchvision import datasets
from torch.utils.data import DataLoader, random_split
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

#import deleteDuplicatePhotos

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

transformWithAugmentation = transforms.Compose([
        transforms.Resize(224),
        transforms.Lambda(pad_to_square),  # Pad dynamically to make the image square
        transforms.Resize((224, 224)),      # Resize to the final size
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor()
    ])

transform = transforms.Compose([
        transforms.Resize(224),
        transforms.Lambda(pad_to_square),  # Pad dynamically to make the image square
        transforms.Resize((224, 224)),      # Resize to the final size
        transforms.ToTensor()
    ])





# Load your hotdog dataset
hotdog_dataset = datasets.ImageFolder(root=classesFolder, transform=transform)


#kinda useless

# Define split sizes (e.g., 80% train, 20% test)
train_size = int(0.9 * len(hotdog_dataset))
test_size = len(hotdog_dataset) - train_size
# Perform the split
train_dataset, test_dataset = random_split(hotdog_dataset, [train_size, test_size])
# Create DataLoaders
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

print(hotdog_dataset.class_to_idx)  


'''
# display random images

import matplotlib.pyplot as plt
import random

image_files = os.listdir(hotdogPhotosPath)
# Select a random image
random_image_path = os.path.join(hotdogPhotosPath, random.choice(image_files))
# Open the image
image = Image.open(random_image_path).convert("RGB")

# Display the image
plt.imshow(image)
plt.title(f"Random Image from Not Hotdog: {random_image_path}")
plt.axis("off")
plt.show()
'''





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

            # Determine label (assuming hotdog = 1, not hotdog = 0)
            labelPrediction = "not hotdog" if confidence >= 0.56 else "hotdog"                     ###########################################################

            # Format confidence
            confidencePercentage = f"{confidence * 100:.2f}%"
            confidenceList = [{labelPrediction: confidencePercentage}]

#        print(f'Prediction: {labelPrediction}\nConfidence: {confidenceList}')
        return labelPrediction, confidenceList



if __name__ == '__main__':

    # Define your binary accuracy function for BCEWithLogitsLoss
    def accuracy_fn(y_true, y_pred):
        # Apply sigmoid to get probabilities then threshold at 0.5
        y_prob = torch.sigmoid(y_pred)
        y_pred_labels = (y_prob > 0.5).float()
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

    # Testing/validation step
    def testStep(model, dataloader, lossFn):
        model.eval()
        total_loss, total_acc = 0, 0

        with torch.no_grad():
            for X, y in dataloader:
                y_pred = model(X)
                loss = lossFn(y_pred, y.unsqueeze(1).float())
                total_loss += loss.item()
                total_acc += accuracy_fn(y, y_pred)

        return total_loss / len(dataloader), total_acc / len(dataloader)





    # Hyperparameters
    epochs = 20
    k_folds = 5
    batch_size = 8
    learning_rate = 0.01



    # Create a DataLoader for the entire dataset
    train_loader = DataLoader(hotdog_dataset, batch_size=batch_size, shuffle=True)

    # Initialize the model (for binary classification, the model should output a single logit)
    model = hotdogLinearModel(inputShape=224*224*3, hiddenUnits=32, outputShape=1)

    # Setup optimizer and loss function (using BCEWithLogitsLoss for binary classification)
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    lossFn = nn.BCELoss()

    # Training loop for the entire dataset
    for epoch in range(epochs):
        train_loss, train_acc = trainStep(model, optimizer, train_loader, lossFn)
        print(f"Epoch {epoch + 1}/{epochs} - Train loss: {train_loss:.5f}, Train acc: {train_acc:.5f}")












    print("--------------------------------------------\n\n\n")
    hotdog = r"glizzy-gobblin-plz-rate-v0-tbbx4xl0i9uc1.webp"
    HPred1, HConf1 = model.predict(hotdog)

    # Open and display the image
    image = Image.open(hotdog).convert("RGB")
    plt.imshow(image)
    plt.title(f"Prediction: {HPred1}")
    plt.axis("off")
    plt.show()


#    torch.save(model.state_dict(), f'hotdogModel.pt')