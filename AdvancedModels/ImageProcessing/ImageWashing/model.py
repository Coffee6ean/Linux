import cv2
import numpy as np

# Read the input image
image = cv2.imread('/home/coffee_6ean/Linux/AdvancedModels/Images/Input/LeanTest_Line_Detection_2.png')

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
cv2.imwrite('preprocessed_image_eroded2.jpg', final_image)
