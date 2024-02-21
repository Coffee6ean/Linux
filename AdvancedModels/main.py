import subprocess

# Define the paths to your scripts
washing_script_path = '/home/coffee_6ean/Linux/AdvancedModels/ImageProcessing/ImageWashing/model.py'
highlighting_script_path = '/home/coffee_6ean/Linux/AdvancedModels/ImageProcessing/ImageHighlight/model.py'
line_detection_script_path = '/home/coffee_6ean/Linux/AdvancedModels/ImageProcessing/LineDetection/model.py'

# Run the image washing script
subprocess.run(['python3', washing_script_path])

# Run the image highlighting script
subprocess.run(['python3', highlighting_script_path])

# Run the line detection script
subprocess.run(['python3', line_detection_script_path])
