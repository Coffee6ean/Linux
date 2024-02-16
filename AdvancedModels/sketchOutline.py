import cv2
import numpy as np

# Load an image
#image = cv2.imread('/home/coffee_6ean/Linux/AdvancedModels/Pictures/sketch_test_1.png')
image = cv2.imread('/home/coffee_6ean/Linux/AdvancedModels/Pictures/LeanTest_Line_Detection_1.PNG')
cv2.imshow('Original Image', image)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply edge detection
edges = cv2.Canny(gray_image, 50, 200, None, 3)

# Detect lines using Hough Line Transform
lines = cv2.HoughLines(edges, 1, np.pi / 180, 150, None, 0, 0)

# Draw detected lines on the original image
if lines is not None:
    for rho, theta in lines[:, 0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Display the original image with detected lines
cv2.imshow('Detected Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
