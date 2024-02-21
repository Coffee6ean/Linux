import cv2
import numpy as np
import os
import sys
sys.path.append("../")
#from ..lib.reusable_methods import load_images_from_folder

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

def highlight_borders(image, kernel_size=(3, 3), iterations=1):
    # Apply dilation
    kernel = np.ones(kernel_size, np.uint8)
    dilated_image = cv2.dilate(image, kernel, iterations=iterations)
    
    # Invert the dilated image back
    highlighted_image = cv2.bitwise_not(dilated_image)
    
    return highlighted_image


# Image Path
input_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/Images/Process/Washing/'
output_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/Images/Process/Highlight/'

# Load images from the input folder
images = load_images_from_folder(input_folder_path)

# Process each image
for idx, image in enumerate(images):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to separate darker lines from lighter areas
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Invert the binary image
    binary = cv2.bitwise_not(binary)

    # Highlight borders using dilation
    highlighted_image = highlight_borders(binary, kernel_size=(2, 2), iterations=2)

    # Save the highlighted image
    output_file_path = os.path.join(output_folder_path, f'highlighted_image_{idx}.jpg')
    cv2.imwrite(output_file_path, highlighted_image)
    print(f"Highlighted image {idx + 1} saved to: {output_file_path}")
