import subprocess

# Define the paths to your scripts
washing_script_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/processing/washing.py'
#dilation_script_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/processing/dilating.py'
opening_script_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/processing/opening.py'
line_detection_script_path = '/home/coffee_6ean/Linux/AdvancedModels/src/models/processing/line_coloring.py'

# Run the image washing script
subprocess.run(['python3', washing_script_path])

# Run the image washing script
subprocess.run(['python3', washing_script_path])

# Run the image opening script
subprocess.run(['python3', opening_script_path])

# Run the image highlighting script
#subprocess.run(['python3', dilation_script_path])

# Run the line detection script
subprocess.run(['python3', line_detection_script_path])
