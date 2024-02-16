import cv2

# Load an image
image = cv2.imread('/home/coffee_6ean/Linux/AdvancedModels/Pictures/sketch_test_1.png')

#--- Preprocessing ---# 
# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the original and preprocessed images
cv2.imshow('Original Image', image)
cv2.imshow('Grayscale Image', gray_image)
#cv2.imshow('Enhanced Image', enhanced_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
