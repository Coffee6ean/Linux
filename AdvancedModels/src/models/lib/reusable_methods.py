import cv2 as cv
import os

def print_file_info(file_path):
    print('###################################')
    print()
    print('#--- Current File Info ---#')
    # Extract file name
    file_name = os.path.basename(file_path)
    
    # Extract folder
    folder = os.path.dirname(file_path)
    
    # Print file name and folder
    print("File Name:", file_name)
    print("Folder:", folder)
    
    # Print methods defined in the file
    print("\nMethods:")
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip().startswith("def "):
                method_name = line.split("(")[0].split("def ")[1]
                print(method_name)
    print()
    print('###################################')

def get_file_path(file_name):
    # Get the absolute path of the current directory
    current_directory = os.path.abspath(os.getcwd())
    
    # Construct the absolute path of the file
    file_path = os.path.join(current_directory, file_name)
    
    return file_path

def load_images_from_path(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

if __name__ == '__main__':
    # Get the file path of the script itself
    current_file_name = os.path.basename(__file__)
    current_file_path = get_file_path(current_file_name)
    
    # Print information about the current file
    print_file_info(current_file_path)
