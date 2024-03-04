import cv2
import numpy as np
import os
import sys
sys.path.append("../")
#from lib.reusable_methods import load_images_from_folder

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

# Image Path
input_folder_path = "/home/coffee_6ean/Linux/AdvancedModels/src/models/images/Process/Opening"
output_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/images/Output'

# Load images from the input folder
images = load_images_from_folder(input_folder_path)
if images:
    print(f"Loaded {len(images)} images from the folder.")
else:
    print("No images found in the folder.")

# Process each image in the array
for i, image in enumerate(images):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use canny edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Apply HoughLinesP method
    lines = cv2.HoughLinesP(
        edges,          # Input edge image
        2,              # Distance resolution in pixels
        np.pi/180,      # Angle resolution in radians
        threshold=80,   # Min number of votes for valid line
        minLineLength=7, # Min allowed length of line
        maxLineGap=7    # Max allowed gap between line for joining them
    )

    # Iterate over detected lines
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Draw the lines on the original image
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Save the result image with an iteration value in the file name
    output_file_path = os.path.join(output_folder_path, f'detected_lines_image_{i}.png')
    cv2.imwrite(output_file_path, image)
    print(f"Preprocessed image {i + 1} saved to: {output_file_path}")

print("All images processed and saved.")
