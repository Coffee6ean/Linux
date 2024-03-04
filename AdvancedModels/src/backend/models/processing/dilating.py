import cv2 as cv
import numpy as np
import os
import sys
sys.path.append("../")
#from ..lib.reusable_methods import *

def load_images_from_path(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

def highlight_borders(image, kernel_size=(3, 3), iterations=1):
    # Apply dilation
    kernel = np.ones(kernel_size, np.uint8)
    dilated_image = cv.dilate(image, kernel, iterations=iterations)
    
    # Invert the dilated image back
    highlighted_image = cv.bitwise_not(dilated_image)
    
    return highlighted_image


# Image Path
input_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/images/Process/Washing'
output_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/images/Process/Dilating'

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

    # Highlight borders using dilation
    highlighted_image = highlight_borders(binary, kernel_size=(2, 2), iterations=2)

    # Save the highlighted image
    output_file_path = os.path.join(output_folder_path, f'highlighted_image_{idx}.jpg')
    cv.imwrite(output_file_path, highlighted_image)
    print(f"Highlighted image {idx + 1} saved to: {output_file_path}")
