import subprocess
import sys
sys.path.append("../")

# Define the paths to your scripts
script1_path = '/home/coffee_6ean/Linux/AdvancedModels/ImageProcessing/ImageWashing/model.py'
script2_path = '/home/coffee_6ean/Linux/AdvancedModels/ImageProcessing/LineDetection/model.py'

# Run the first script
subprocess.run(['python', script1_path])

# Once the first script finishes, move the resulting image to a folder
# This assumes that the script1.py script saves the washed image as 'washed_image.jpg'
subprocess.run(['mv', 'washed_image.jpg', 'path/to/your/output/folder/'])

# Run the second script, which performs line detection on the washed image
subprocess.run(['python', script2_path])
