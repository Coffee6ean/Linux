import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Read the input image
image = cv.imread('/home/coffee_6ean/Linux/AdvancedModels/src/models/images/Input/LeanTest_2.png')

# Apply Gaussian blur
blurred_image = cv.GaussianBlur(image, (5, 5), 0)

# Save the blurred image
cv.imwrite('/home/coffee_6ean/Linux/AdvancedModels/src/models/test_image_blur.jpg', blurred_image)
