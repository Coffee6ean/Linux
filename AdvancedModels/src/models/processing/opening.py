import cv2 as cv
import numpy as np
import os
import sys

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

def preprocess_image(image):
    # Convert to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding
    _, binary = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    
    return binary

# Function to perform opening operation
def perform_opening(image, kernel_size=(3, 3), iterations=1):
    # Define the kernel for opening operation
    kernel = np.ones(kernel_size, np.uint8)
    
    # Apply opening operation with specified iterations
    opening = cv.morphologyEx(image, cv.MORPH_OPEN, kernel, iterations=iterations)
    
    return opening

# Image Path
input_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/images/Process/Washing'
output_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/models/Images/Process/Opening'

# Load images from the input folder
images = load_images_from_folder(input_folder_path)

# Process each image
for idx, image in enumerate(images):
    # Preprocess the image
    preprocessed_image = preprocess_image(image)
    
    # Perform opening operation
    opened_image = perform_opening(preprocessed_image, (4, 4), 10)

    # Save the opened image
    output_file_path = os.path.join(output_folder_path, f'opened_image_{idx}.jpg')
    cv.imwrite(output_file_path, opened_image)
    print(f"Opened image {idx + 1} saved to: {output_file_path}")
