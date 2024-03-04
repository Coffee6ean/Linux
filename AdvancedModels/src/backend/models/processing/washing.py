# System Imports
import cv2 as cv
import numpy as np
import os
import sys

# Append Parent Directory to sys.path
sys.path.append('../')

# Helper functions
#from ..lib.reusable_methods import * 

def load_images_from_path(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

# Image Path
input_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/images/Input'
output_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/images/Process/Washing'

# Load images from the input folder
images = load_images_from_path(input_folder_path)

# Process each image
for idx, image in enumerate(images):
    # Convert the image to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Apply a binary threshold to separate darker lines from lighter areas
    _, binary = cv.threshold(gray, 128, 255, cv.THRESH_BINARY)

    # Invert the binary image
    binary = cv.bitwise_not(binary)

    # Perform erosion
    kernel = np.ones((2, 2), np.uint8)  # Define a 2x2 kernel for erosion
    eroded_image = cv.erode(binary, kernel, iterations=1)

    # Invert the colors again to get white background and black lines
    final_image = cv.bitwise_not(eroded_image)

    # Save the preprocessed image with erosion
    output_file_path = os.path.join(output_folder_path, f'preprocessed_image_eroded_{idx}.jpg')
    cv.imwrite(output_file_path, final_image)
    print(f"Preprocessed image {idx + 1} saved to: {output_file_path}")
