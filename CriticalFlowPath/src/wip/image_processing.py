import os
import re
import cv2 as cv
import pandas as pd
import numpy as np
import pytesseract
from collections import Counter
from PIL import Image

class ImageProcessing:
    def __init__(self, input_images_path, output_images_path):
        self.input_path = input_images_path    
        self.output_path = output_images_path
        self.wbs_directory = None

    @staticmethod
    def main():
        project = ImageProcessing.generate_ins()
        #project.select_wbs_region(project.input_path, "wbs_table")
        #project.color_slice_tasks(os.path.join(project.output_path, "wbs_table"), "wbs_tasks")
        #project.sharpen_project_images(os.path.join(project.output_path, "wbs_table"), "wbs_tasks")
        #project.write_wbs_file(os.path.join(project.output_path, "wbs_table"), "wbs_tasks", "wbs_files")
        project.clean_project_text(project.output_path, project.output_path, "clean_test")

    @staticmethod
    def generate_ins():
        input_images_path = input("Enter the image(s) directory to process: ")
        output_images_path = input("Enter the file directory to save the processed images: ")

        return ImageProcessing(input_images_path, output_images_path)

    @staticmethod
    def bubble_sort_str_list(img_dir):
        images = os.listdir(img_dir)  # List all images in the directory

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
    def visualize_horizontal_lines(img_dir, min_line_width=100):
        image = cv.imread(img_dir)

        if image is None:
            print(f"Error: Could not read image {img_dir}.")
            return

        # Convert to grayscale
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        # Threshold to isolate dark (black) areas; adapt threshold value to your images if needed
        _, binary = cv.threshold(gray, 50, 255, cv.THRESH_BINARY_INV)

        # Detect horizontal lines using morphological operations
        horizontal_kernel = cv.getStructuringElement(cv.MORPH_RECT, (50, 1))  # Larger kernel for better detection
        horizontal_lines = cv.morphologyEx(binary, cv.MORPH_OPEN, horizontal_kernel)

        # Find contours representing the lines
        contours, _ = cv.findContours(horizontal_lines, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Filter contours based on minimum width
        filtered_contours = []
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            if w >= min_line_width:  # Only keep contours with width >= min_line_width
                filtered_contours.append(contour)

        # Visualize the filtered contours on the image
        debug_image = image.copy()
        cv.drawContours(debug_image, filtered_contours, -1, (0, 255, 0), 2)  # Green contours for filtered lines

        # Display the image with filtered contours
        cv.imshow("Filtered Contours (Largest Horizontal Black Lines)", debug_image)
        cv.waitKey(0)  # Wait indefinitely until a key is pressed
        cv.destroyAllWindows()  # Close the window after key press

        print(f"Filtered contours visualized for: {img_dir}")

    @staticmethod
    def slice_based_on_color_change(img_dir, output_dir, color_change_threshold=50):
        image = cv.imread(img_dir)

        if image is None:
            print(f"Error: Could not read image {img_dir}.")
            return

        # Convert image to Lab color space (perceptually uniform)
        lab_image = cv.cvtColor(image, cv.COLOR_BGR2Lab)

        # Get image dimensions
        height, width, _ = lab_image.shape

        # List to store slice boundaries
        slice_boundaries = []

        # Loop through rows and calculate color differences between consecutive rows
        for y in range(1, height):
            row1 = lab_image[y - 1, :, :]
            row2 = lab_image[y, :, :]

            # Calculate the mean color for each row
            mean_row1 = cv.mean(row1)[:3]
            mean_row2 = cv.mean(row2)[:3]

            # Calculate the Euclidean distance between the mean colors of the rows
            color_difference = np.sqrt(sum((mean_row2[i] - mean_row1[i]) ** 2 for i in range(3)))

            # If the color difference exceeds the threshold, mark it as a slice boundary
            if color_difference > color_change_threshold:
                slice_boundaries.append(y)

        # Slice the image at detected color change boundaries
        task_slices = []
        previous_boundary = 0

        for boundary in slice_boundaries:
            task_slice = image[previous_boundary:boundary, :]  # Slice from previous boundary to current boundary
            task_slices.append(task_slice)
            previous_boundary = boundary

        # Add the last slice (from the last boundary to the bottom of the image)
        if previous_boundary < height:
            task_slices.append(image[previous_boundary:, :])

        # Save each slice with a unique name
        for idx, task_slice in enumerate(task_slices):
            save_path = os.path.join(output_dir, f"task_slice_{idx}.png")
            cv.imwrite(save_path, task_slice)

        #print(f"Image {img_dir} sliced into {len(task_slices)} pieces based on color change.")

    @staticmethod
    def sharpen_image(img_dir):
        image = cv.imread(img_dir)

        if image is None:
            print(f"Error: Could not read image {img_dir}.")
            return

        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened_image = cv.filter2D(image, -1, kernel)

        try:
            cv.imwrite(img_dir, sharpened_image)
            print(f"Sharpened image saved successfully to {img_dir}")
        except Exception as e:
            print(f"Error: Could not save image to {img_dir}. Exception: {e}")

    @staticmethod
    def extract_text_from_image(img_dir, output_path, output_basename, mode='a'):
        try:
            image = Image.open(img_dir)
            text = pytesseract.image_to_string(image)

            # Ensure the output path exists (but not the file itself)
            os.makedirs(output_path, exist_ok=True)

            # Full path for the output text file (append ".txt" to the basename)
            output_file = os.path.join(output_path, f"{output_basename}.txt")

            # Write the extracted text to the file
            with open(output_file, mode) as file:
                file.write(text + "\n")  # Append a newline after each text block
        except Exception as e:
            print(f"Error: Unable to write to file at {output_file}. Exception: {e}")

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

    @staticmethod
    def get_type_files(input_dir, file_type):
        file_list = []

        if os.path.isfile(input_dir):
            if input_dir.endswith(file_type):
                file_list.append(os.path.abspath(input_dir))
            else:
                print(f"Error: The file '{input_dir}' does not match the specified type '{file_type}'.")

        elif os.path.isdir(input_dir):
            files = os.listdir(input_dir)
            for file in files:
                if file.endswith(file_type):
                    file_path = os.path.join(input_dir, file)
                    file_list.append(os.path.abspath(file_path))

        else:
            print(f"Error: '{input_dir}' is neither a valid file nor a directory.")

        return file_list

    def repackage_files_in_dir(self, input_dir):
        sorted_files = ImageProcessing.bubble_sort_str_list(input_dir)

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
        sorted_list = ImageProcessing.bubble_sort_str_list(img_dir)
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
        sorted_images = ImageProcessing.bubble_sort_str_list(img_dir)

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

    def detect_horizontal_lines(self, input_dir, min_line_width=100):
        sorted_packages = ImageProcessing.bubble_sort_str_list(input_dir)
        images = []

        for package in sorted_packages:
            package_dir = os.path.join(input_dir, package)
            images.append(ImageProcessing.get_type_files(package_dir, "jpg")[0])
        
        all_contours = []  

        for img_dir in images:
            image = cv.imread(img_dir)
            
            if image is None:
                continue
            
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            _, binary = cv.threshold(gray, 50, 255, cv.THRESH_BINARY_INV)

            # Use morphological operations to detect horizontal lines
            horizontal_kernel = cv.getStructuringElement(cv.MORPH_RECT, (40, 1))
            horizontal_lines = cv.morphologyEx(binary, cv.MORPH_OPEN, horizontal_kernel)

            # Find contours representing the lines
            contours, _ = cv.findContours(horizontal_lines, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            # Filter contours based on minimum width
            filtered_contours = []
            for contour in contours:
                x, y, w, h = cv.boundingRect(contour)
                if w >= min_line_width:  # Only keep contours with width >= min_line_width
                    filtered_contours.append(contour)
            
            # Store contours associated with the current image
            all_contours.append((img_dir, filtered_contours))

        return all_contours  # Return a list of tuples (image_name, contours)

    def line_slice_tasks(self, input_dir, new_directory):
        # Detect horizontal lines in the images
        detected_contours = self.detect_horizontal_lines(input_dir)

        for img_dir, contours in detected_contours:
            # Read the image again for slicing
            image = cv.imread(img_dir)

            # Ensure the output directory exists
            output_dir = os.path.join(os.path.dirname(img_dir), new_directory)
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            
            if image is None:
                print(f"Warning: Could not read image {img_dir}. Skipping.")
                continue  # Skip if the image is not found or corrupted

            # Sort contours by their Y-coordinate to slice the regions in order
            contours = sorted(contours, key=lambda c: cv.boundingRect(c)[1])

            task_slices = []
            height, width = image.shape[:2]

            # Process the regions between the lines
            prev_y = 0  # Start from the top of the image
            for contour in contours:
                x, y, w, h = cv.boundingRect(contour)

                # Slice the region between the previous line and the current line
                task_slice = image[prev_y:y, :]  # Slice the rows between the previous Y and current Y
                task_slices.append(task_slice)

                prev_y = y + h  # Update prev_y to the bottom of the current contour

            # Handle the area below the last line, if any
            if prev_y < height:
                task_slice = image[prev_y:height, :]
                task_slices.append(task_slice)

            # Save the slices
            self.save_task_slices(task_slices, output_dir, img_dir)

    def color_slice_tasks(self, input_dir, new_directory):
        sorted_packages = ImageProcessing.bubble_sort_str_list(input_dir)
        images = []

        for package in sorted_packages:
            package_dir = os.path.join(input_dir, package)
            jpg_files = ImageProcessing.get_type_files(package_dir, "jpg")
            if jpg_files:
                images.append(jpg_files[0])

        for image in images:
            output_dir = os.path.join(os.path.dirname(image), new_directory)
            os.makedirs(output_dir, exist_ok=True)

            self.slice_based_on_color_change(image, output_dir)

    def sharpen_project_images(self, input_dir, directory):
        sorted_packages = ImageProcessing.bubble_sort_str_list(input_dir)

        for package in sorted_packages:
            tasks_dir = os.path.join(input_dir, package)
            images_dir = os.path.join(tasks_dir, directory)

            project_images = ImageProcessing.bubble_sort_str_list(images_dir)

            for image in project_images:
                image_dir = os.path.join(images_dir, image)
                ImageProcessing.sharpen_image(image_dir)

        print("Project images succesfully sharpened")

    def write_wbs_file(self, input_dir, directory, new_directory, mode='a'):
        sorted_packages = ImageProcessing.bubble_sort_str_list(input_dir)

        for package in sorted_packages:
            tasks_dir = os.path.join(input_dir, package)
            images_dir = os.path.join(tasks_dir, directory)

            project_images = ImageProcessing.bubble_sort_str_list(images_dir)

            for image in project_images:
                image_dir = os.path.join(images_dir, image)

                # Extract text from the image and append it to the output text file
                ImageProcessing.extract_text_from_image(image_dir, self.output_path, "test", mode)

        print("Project text file succesfully created")

    def clean_project_text(self, input_dir, output_path, output_basename, mode='w'):
        if not os.path.exists(input_dir):
            print(f"Error: Input file {input_dir} does not exist.")
            return
        
        file_dir = ImageProcessing.get_type_files(input_dir, 'txt')[0]
        
        with open(file_dir, 'r') as file_reader:
            input_text = file_reader.read()

        clean_text = re.sub('\n+', ' ', input_text)
        normalized_text = re.sub('\s{2,}', '\n', clean_text)

        output_dir = os.path.join(output_path, f"{output_basename}.txt")

        with open(output_dir, mode) as file_writer:
            file_writer.write(normalized_text)

        print("Project text file succesfully cleaned & normalized")

    def save_task_slices(self, task_slices, input_dir, image_name):
        # Ensure the save folder exists
        os.makedirs(input_dir, exist_ok=True)

        # Save each task slice with a unique name
        for idx, task_slice in enumerate(task_slices):
            if task_slice is None or task_slice.size == 0:  # Check if the slice is valid
                print(f"Warning: Skipping empty or invalid task slice {idx}.")
                continue  # Skip if the slice is empty or invalid

            base_name, ext = os.path.splitext(image_name)
            save_path = os.path.join(input_dir, f"task_{idx}.png")
            
            # Now try saving the slice
            success = cv.imwrite(save_path, task_slice)
            if not success:
                print(f"Error: Failed to save task slice {idx} to {save_path}.")
            else:
                print(f"Task slice {idx} saved successfully at {save_path}.")

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
