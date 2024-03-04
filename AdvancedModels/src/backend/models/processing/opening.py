import cv2 as cv
import numpy as np
import os

#--- Functions ---#
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

def perform_opening(image, kernel_size=(2,2), iterations=1):
    # Define the kernel for morphology operation
    kernel = np.ones(kernel_size, np.uint8)

    # Apply opening operation iteratively
    opening = cv.morphologyEx(image, cv.MORPH_OPEN, kernel, iterations=iterations)

    return opening

def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Apply a binary threshold to separate darker lines from lighter areas
    _, binary = cv.threshold(gray, 128, 255, cv.THRESH_BINARY)

    # Invert the binary image
    binary = cv.bitwise_not(binary)

    return binary

#--- Code Block ---#
# Image Path
input_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/images/Process/Washing'
output_folder_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/images/Process/Opening'

# Load images from the input folder
images = load_images_from_folder(input_folder_path)

for idx, image in enumerate(images):
    # Preprocess the image
    preprocessed_image = preprocess_image(image)

    # Perform opening operation
    opened_image = perform_opening(preprocessed_image)

    # Save the opened image 
    output_file_path = os.path.join(output_folder_path, f'opened_image_{idx}.jpg')
    cv.imwrite(output_file_path, opened_image)


if __name__ == '__main__':
    image_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/test_image_blur.jpg'

    img = cv.imread(image_path)

    # Preprocess the image
    preprocessed_image = preprocess_image(img)

    # Perform opening operation
    opened_image = perform_opening(preprocessed_image)

    # Save the opened image
    cv.imwrite('/home/coffee_6ean/Linux/AdvancedModels/src/models/test_image_opened.jpg', opened_image)
