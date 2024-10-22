import os
import re
import cv2 as cv
import pandas as pd
import numpy as np
import pytesseract
from collections import Counter
from PIL import Image, ImageFilter, ImageEnhance

class ImageProcessing:
    def __init__(self, input_images_path, output_images_path):
        self.input_path = input_images_path    
        self.output_path = output_images_path

    @staticmethod
    def main():
        project = ImageProcessing.generate_ins()
        project.select_wbs_region(project.input_path, "wbs_table")
        #project.detect_horizontal_lines(os.path.join(project.input_path, "wbs_table"))
        #project.slice_tasks()

    @staticmethod
    def generate_ins():
        input_images_path = input("Enter the image(s) directory to process: ")
        output_images_path = input("Enter the file directory to save the processed images: ")

        return ImageProcessing(input_images_path, output_images_path)

    @staticmethod
    def bubble_sort(img_list):
        images = os.listdir(img_list)  # List all images in the directory

        n = len(images)
        
        for i in range(n):
            swap = False  # Track if a swap was made in this pass

            # Iterate through the unsorted portion of the list
            for j in range(n - 1 - i):  # `- i` ensures we don't re-check sorted elements
                
                # Extract numeric part of the filenames using regex
                img_id = re.search(r'\d+', images[j])
                one_plus_img_id = re.search(r'\d+', images[j + 1])
                
                # Convert regex matches to integers for comparison, default to 0 if no match
                img_id = int(img_id.group()) if img_id else 0
                one_plus_img_id = int(one_plus_img_id.group()) if one_plus_img_id else 0

                # Compare the extracted numeric parts
                if img_id > one_plus_img_id:
                    # Swap elements using Python's tuple unpacking
                    images[j], images[j + 1] = images[j + 1], images[j]
                    swap = True

            # If no swaps were made, the list is already sorted
            if not swap:
                break

        return images

    @staticmethod
    def package_file(input_dir, package_name=None):
        if os.path.isfile(input_dir):
            file_path = os.path.dirname(input_dir)
            file_basename = os.path.basename(input_dir)
            file_extension = os.path.splitext(file_basename)[1]
            new_directory_basename = os.path.splitext(file_basename)[0]

            if isinstance(package_name, str):
                new_directory = os.path.join(file_path, package_name)
            else:
                new_directory = os.path.join(file_path, new_directory_basename)

            if not os.path.exists(new_directory):
                os.mkdir(new_directory)

            new_file_name = f"packaged_{new_directory_basename}{file_extension}"
            new_file_path = os.path.join(new_directory, new_file_name)

            try:
                os.rename(input_dir, new_file_path)
            except Exception as e:
                print(f"Error moving the file {input_dir} to {new_file_path}: {e}")
        else:
            print(f"{input_dir} is not a valid file.")

    def repackage_files_in_dir(self, input_dir):
        sorted_files = ImageProcessing.bubble_sort(input_dir)

        for i, file in enumerate(sorted_files):
            file_path = os.path.join(input_dir, file)
            ImageProcessing.package_file(file_path, f"package_page_{i}")

        print("Files successfully repackaged")

    def select_wbs_region(self, input_dir, new_directory, roi_msg="Select WBS Region"):
        self.crop_image(input_dir, new_directory, roi_msg)
        cv.destroyWindow(roi_msg)

    def crop_image(self, input_dir, new_directory, roi_msg=False):
        if roi_msg == False:
            roi_msg = "Select the area"

        if os.path.isfile(input_dir):
            self._crop_single_image(input_dir, new_directory, roi_msg)
        
        elif os.path.isdir(input_dir):
            self._crop_multiple_images(input_dir, new_directory, roi_msg)
        
        else:
            print(f"Error: {input_dir} is neither a valid file nor a directory.")

    def _crop_single_image(self, img_dir, new_directory, roi_msg):
        sorted_list = ImageProcessing.bubble_sort(img_dir)
        image = sorted_list[0]
        
        if image is None:
            print(f"Error: Could not read image {img_dir}.")
            return

        r = cv.selectROI(roi_msg, image)
        cropped_image = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

        output_basename = "cropped_img_0.jpg"
        output_dir = os.path.join(self.output_path, new_directory)

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        output_path = os.path.join(output_dir, output_basename)
        cv.imwrite(output_path, cropped_image)

    def _crop_multiple_images(self, img_dir, new_directory, roi_msg):
        sorted_images = ImageProcessing.bubble_sort(img_dir)

        if not sorted_images:
            print(f"Error: No images found in directory {img_dir}.")
            return

        first_image_path = os.path.join(img_dir, sorted_images[0])
        first_image = cv.imread(first_image_path)

        if first_image is None:
            print(f"Error: Could not read image {first_image_path}.")
            return

        r = cv.selectROI(roi_msg, first_image)
        output_dir = os.path.join(self.output_path, new_directory)
        
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        for i, img_name in enumerate(sorted_images):
            img_path = os.path.join(img_dir, img_name)
            image = cv.imread(img_path)

            if image is None:
                print(f"Warning: Could not read image {img_path}. Skipping.")
                continue

            cropped_image = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

            output_basename = f"cropped_img_{i}.jpg"
            output_path = os.path.join(output_dir, output_basename)
            
            cv.imwrite(output_path, cropped_image)
        
        self.repackage_files_in_dir(output_dir)

    def sharpen_image(self):
        # Load the image 
        image = cv.imread("/home/coffee_6ean/Linux/CriticalFlowPath/src/local_results/proc_images/cropped/cropped_img_0.jpg") 
        
        # Create the sharpening kernel 
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) 
        
        # Sharpen the image 
        sharpened_image = cv.filter2D(image, -1, kernel) 
        
        #Save the image 
        output_file_name = f"sharpened_img_{1}.jpg"
        output_path = "/home/coffee_6ean/Linux/CriticalFlowPath/src/local_results/proc_images/sharpened"
        output_dir = os.path.join(output_path, output_file_name)
        
        cv.imwrite(output_dir, sharpened_image)

    def image_to_text(self, img_dir, file_name):
        image = Image.open(img_dir)
        text = pytesseract.image_to_string(image)
        
        output_path = "/home/coffee_6ean/Linux/CriticalFlowPath/src/local_results"
        output_basename = file_name
        output = os.path.join(output_path, output_basename)
        f1 = open(output, 'w')
        f1.write(text)

    def load_color_data(self, csv_file):
        # Load the CSV into a pandas DataFrame
        df = pd.read_csv(csv_file, header=None, names=['color_id', 'color_name', 'hex_code', 'r', 'g', 'b'])
        
        # Convert the RGB columns to a tuple for dictionary lookup
        df['rgb_tuple'] = list(zip(df['r'], df['g'], df['b']))
        
        return df

    def detect_colors(self, exclude_black_white=True):
        image_path = "/home/coffee_6ean/Linux/CriticalFlowPath/src/local_results/proc_images/sharpened"
        image_basename = "sharpened_img_1.jpg"
        image_dir = os.path.join(image_path, image_basename)
        
        # Read the image
        image = cv.imread(image_dir)
        
        # Convert to HSV for better color distinction
        hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        
        # Reshape the image to be a list of pixels
        pixels = hsv_image.reshape(-1, 3)
        
        # Optional: Exclude black and white by setting thresholds for brightness and saturation
        if exclude_black_white:
            # Filter out near-black pixels (low brightness) and near-white (low saturation)
            mask = (pixels[:, 2] > 30) & (pixels[:, 1] > 50)  # Adjust thresholds as needed
            pixels = pixels[mask]
        
        # Convert the remaining HSV colors back to RGB
        rgb_pixels = cv.cvtColor(pixels.reshape(-1, 1, 3), cv.COLOR_HSV2BGR).reshape(-1, 3)
        
        # Use a Counter to count the occurrence of each color
        color_counts = Counter(map(tuple, rgb_pixels))
        
        # Get the most common colors, sorted by frequency
        common_colors = color_counts.most_common()
        
        # Return the detected colors as a list of (color, count) tuples
        return common_colors

    def process_colors(self, color_list):
        # Create a set to store unique colors
        unique_colors = set()

        for color, count in color_list:
            # Convert the color tuple to a string and add to the set
            color_str = f"({color[0]}, {color[1]}, {color[2]})"
            unique_colors.add(color_str)

        return unique_colors

    def get_color_name(self, R, G, B, color_data):
        # Convert the pixel values to int to avoid overflow
        R, G, B = int(R), int(G), int(B)

        # Initialize the minimum distance with a large value and a placeholder for the closest color name
        minimum_distance = float('inf')
        closest_color_name = None

        # Iterate through the color data to find the closest color
        for i in range(len(color_data)):
            csv_R, csv_G, csv_B = color_data.iloc[i]['rgb_tuple']  # Extract the RGB tuple
            csv_R, csv_G, csv_B = int(csv_R), int(csv_G), int(csv_B)  # Convert to int

            # Calculate the Manhattan distance (sum of absolute differences)
            distance = abs(R - csv_R) + abs(G - csv_G) + abs(B - csv_B)

            # If the current distance is smaller, update the minimum distance and closest color name
            if distance < minimum_distance:
                minimum_distance = distance
                closest_color_name = color_data.iloc[i]['color_name']

        return closest_color_name

    def find_closest_color_names(self, detected_colors, color_data):
        # List to store results
        color_name_results = []

        for rgb_tuple, count in detected_colors:
            R, G, B = rgb_tuple

            # Get the closest color name
            closest_color_name = self.get_color_name(R, G, B, color_data)
            
            # Append to the results list
            color_name_results.append((closest_color_name, count))

        return color_name_results

    def return_color_list(self):
        # Load the color data from the CSV
        csv_file = "/home/coffee_6ean/Linux/CriticalFlowPath/src/lib/colors.csv"
        color_data = self.load_color_data(csv_file)

        # Detect colors from the image
        detected_colors = self.detect_colors(exclude_black_white=True)

        # Process and find the closest color names
        closest_colors = self.find_closest_color_names(detected_colors, color_data)

        # Print the results
        for color_name, count in closest_colors:
            print(f"Color: {color_name}, Count: {count}")


if __name__ == "__main__":
    ImageProcessing.main()