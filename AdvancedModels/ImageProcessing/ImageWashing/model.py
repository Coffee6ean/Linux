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


# Image Path
input_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/Images/Input'
output_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/Images/Process'

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

    # Perform erosion
    kernel = np.ones((2, 2), np.uint8)  # Define a 2x2 kernel for erosion
    eroded_image = cv2.erode(binary, kernel, iterations=2)

    # Invert the colors again to get white background and black lines
    final_image = cv2.bitwise_not(eroded_image)

    # Save the preprocessed image with erosion
    output_file_path = os.path.join(output_folder_path, f'preprocessed_image_eroded_{idx}.jpg')
    cv2.imwrite(output_file_path, final_image)
    print(f"Preprocessed image {idx + 1} saved to: {output_file_path}")
