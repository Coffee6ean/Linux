import os
import re
import json
import cv2 as cv
import numpy as np
import pytesseract
from datetime import datetime
from pdf2image import convert_from_path
from PIL import Image

import sys
sys.path.append("../")
from CriticalFlowPath.keys.secrets import TEST_PDF_DIR

class PdfDataIngestion:
    allowed_extensions = ["pdf"]
    project_pages = 1

    def __init__(self, input_file_path, input_file_basename, input_file_extension) -> None:
        self.input_path = input_file_path
        self.input_basename = input_file_basename
        self.input_extension = input_file_extension

        #Module Attributes
        self.sorted_image_list = []

    @staticmethod
    def main(auto=True, input_file_path=None, input_file_basename=None, input_file_extension=None):
        if auto:
            project = PdfDataIngestion.auto_generate_ins(input_file_path, input_file_basename, input_file_extension)
        else:
            project = PdfDataIngestion.generate_ins()

        if project:
            file_basename = f"{project.input_basename}.{project.input_extension}" 
            file = os.path.join(project.input_path, file_basename) 
            output_folder = f"{TEST_PDF_DIR}/{PdfDataIngestion.return_valid_date()}"
            os.makedirs(output_folder, exist_ok=True)
            
            project.pdf_to_images(file, output_folder)
            project.resize_images(output_folder)
            project.process_images(output_folder)
            #project.clean_project_text(output_folder, output_folder, "test")

    @staticmethod
    def generate_ins():
        input_file = PdfDataIngestion.return_valid_file(
            input("Please enter the path to the file or directory: ").strip()
        )

        ins = PdfDataIngestion(
            input_file.get("path"), 
            input_file.get("basename"), 
            input_file.get("extension")
        )

        return ins

    @staticmethod
    def auto_generate_ins():
        pass

    @staticmethod
    def return_valid_file(input_file_dir:str) -> dict|int:
        if not os.path.exists(input_file_dir):
            raise FileNotFoundError("Error: Given directory or file does not exist in the system.")

        if os.path.isdir(input_file_dir):
            file_dict = PdfDataIngestion._handle_dir(input_file_dir)
        elif os.path.isfile(input_file_dir):
            file_dict = PdfDataIngestion._handle_file(input_file_dir)

        return file_dict
    
    @staticmethod
    def _handle_dir(input_file_dir:str, mode:str="r") -> dict|int:
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_file_dir)
            selection = PdfDataIngestion._display_directory_files(dir_list)
            input_file_basename = dir_list[selection]
            print(f'File selected: {input_file_basename}\n')
        elif mode == 'c':
            input_file_basename = None
        else:
            print("Error: Invalid mode specified.")
            return -1
        
        return dict(
            path = os.path.dirname(input_file_dir), 
            basename = os.path.basename(input_file_basename).split(".")[0],
            extension = os.path.basename(input_file_basename).split(".")[-1],
        )
    
    @staticmethod
    def _display_directory_files(file_list:list) -> int:
        selection_idx = -1  

        if len(file_list) == 0:
            print('Error. No files found')
            return -1
        
        print(f'-- {len(file_list)} files found:')
        for idx, file in enumerate(file_list, start=1):  
            print(f'{idx}. {file}')

        while True:
            try:
                selection_idx = int(input('\nPlease enter the index number to select the one to process: '))
                if 1 <= selection_idx <= len(file_list):  
                    return selection_idx - 1  
                else:
                    print(f'Error: Please enter a number between 1 and {len(file_list)}.')
            except ValueError:
                print('Error: Invalid input. Please enter a valid number.\n')

    @staticmethod
    def _handle_file(input_file_dir:str) -> dict|int:
        input_file_extension = os.path.basename(input_file_dir).split(".")[-1]

        if (input_file_extension in PdfDataIngestion.allowed_extensions):
            return dict(
                path = os.path.dirname(input_file_dir), 
                basename = os.path.basename(input_file_dir).split(".")[0],
                extension = input_file_extension,
            )

        print("Error: Please verify that the directory and file exist and that the file extension complies with class attributes")
        return -1

    @staticmethod
    def return_valid_path(prompt_message:str) -> (str|None):
        while(True):   
            value = input(prompt_message).strip()
            try:
                if os.path.isdir(value):
                    return value
            except Exception as e:
                print(f"Error. {e}\n")

    @staticmethod
    def return_valid_date() -> str:
        now = datetime.now()
        date_str = now.strftime("%d-%b-%y %H:%M:%S")

        return date_str

    @staticmethod
    def get_type_files(input_dir:str, file_type:str) -> list:
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

    @staticmethod
    def repackage_file(input_dir:str, package_name:str=None) -> str:
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

        return new_file_path

    @staticmethod
    def slice_based_on_color_change(image_path:str, output_dir:str, image_extension:str, 
                                     color_change_threshold:int=50) -> None:
        os.makedirs(output_dir, exist_ok=True)
        image = cv.imread(image_path)

        if image is None:
            print(f"Error: Could not read image '{image_path}'")
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
            save_path = os.path.join(output_dir, f"image_slice_{idx+1}.{image_extension}")
            cv.imwrite(save_path, task_slice)

    @staticmethod
    def extract_data_from_image(image_path:str, output_path:str, output_basename:str, file_extension:str,
                                mode:str='a', tesseract_config:str="--psm 4") -> str:
        try:
            if os.stat(image_path).st_size >= 5000:
                image = Image.open(image_path)
                text = pytesseract.image_to_string(image, config=tesseract_config)

                os.makedirs(output_path, exist_ok=True)
                output_file = os.path.join(output_path, f"{output_basename}.{file_extension}")
                
                cleaned_text = PdfDataIngestion._normalize_file_text(text)

                return cleaned_text
        except Exception as e:
            print(f"Error: Unable to write to file at '{output_file}'. Exception: {e}")

    @staticmethod
    def _normalize_file_text(text_body: str) -> str:
        empty_lines = re.compile('^\s*$', re.MULTILINE)
        removed_empty_lines = re.sub(empty_lines, "", text_body)

        whitespace_lines = re.compile('^\n', re.MULTILINE)
        removed_whitespace_lines = re.sub(whitespace_lines, "", removed_empty_lines)

        removed_whitespace_lines = removed_whitespace_lines.strip()
        
        return removed_whitespace_lines

    @staticmethod
    def jsonify_project_data(text_body: str) -> list:
        text_lines = [line.strip() for line in text_body.split('\n') if line.strip()]
        proc_dict = {
            "header": {"page": PdfDataIngestion.project_pages},
            "body": {
                "details": {"activities": {"total": 0}},
                "logs": [],
                "content": [],
            },
        }
        
        for i, line in enumerate(text_lines, 1):
            try:
                match = PdfDataIngestion.test_pattern(line)
                if not match:
                    match = PdfDataIngestion.special_pattern(line)
                    if not match:
                        proc_dict["body"]["logs"].append({
                            "task": i,
                            "content": line,
                            "parse_error": True
                        })
                        continue

                groups = match.groupdict()
                
                def clean(value):
                    return value.strip() if value and isinstance(value, str) else ""
                
                start_date = clean(groups.get("StartDate") or groups.get("StartDateAlt"))
                finish_date = clean(groups.get("FinishDate"))
                start_day = clean(groups.get("StartDay") or groups.get("StartDay1") or groups.get("StartDay2"))
                finish_day = clean(groups.get("FinishDay") or groups.get("FinishDay1"))
                start = f"{start_day} {start_date}".strip() if start_day and start_date else start_date or ""
                finish = f"{finish_day} {finish_date}".strip() if finish_day and finish_date else finish_date or ""
                
                deps = groups.get("Dependencies", "")
                if deps:
                    predecessors = [dep.strip() for dep in str(deps).split(',') if dep.strip()]
                else:
                    predecessors = []
                
                task = {
                    "entry": i,
                    "wbs_code": clean(groups.get("ActivityCode")),
                    "activity_name": clean(groups.get("ActivityName")),
                    "percentage_complete": clean(groups.get("PercentageComplete")),
                    "duration": clean(groups.get("Duration")),
                    "start_date": start,
                    "finish_date": finish,
                    "predecessors": predecessors
                }
                
                proc_dict["body"]["content"].append(task)
                proc_dict["body"]["details"]["activities"]["total"] += 1
                
            except Exception as e:
                proc_dict["body"]["logs"].append({
                    "task": i,
                    "content": line,
                    "parse_error": True,
                    "error": str(e)
                })
        
        PdfDataIngestion.project_pages += 1
        return proc_dict

    @staticmethod
    def standard_pattern(text:str):
        pattern = re.compile(
            r"(?P<ActivityID>(?:[A-Z]{2,}(?:-[A-Z0-9]+)*-\d+|[A-Z]+(?:-[A-Z0-9]+){2,}))"
            r"(?P<ActivityName>.*?)\s+"
            r"(?P<Duration>\d+d)\s*"
            r"(?P<Dates>(?:\d{2}-[A-Za-z]{3}-\d{2}[A*]?(?:\s+\d{2}-[A-Za-z]{3}-\d{2}[A*]?)?))",
            re.DOTALL | re.IGNORECASE
        )

        return pattern.match(text)

    @staticmethod
    def special_pattern(text:str):
        special_chars = re.compile('[+=—@_!#$%^&*<>?/\|}{~:]')
        remove_special_chars = re.sub(special_chars, '', text)

        pattern = re.compile(
            r"(?P<ActivityID>(?:[A-Z]{2,}(?:-[A-Z0-9]+)*-\d+|[A-Z]+(?:-[A-Z0-9]+){2,})|)"
            r"(?P<ActivityName>.*?)\s+"
            r"(?P<Duration>(\d+d)|)\s*"
            r"(?P<Dates>(?:\d{2}-[A-Za-z]{3}-\d{2}[A*]?(?:\s+\d{2}-[A-Za-z]{3}-\d{2}[A*]?)?))",
            re.DOTALL | re.IGNORECASE
        )

        r"(?P<Duration>((\d{3,})+d)|((\d{3,})+\S)|)\s*"

        return pattern.match(remove_special_chars)
    
    @staticmethod
    def test_pattern(text: str):
        special_chars = re.compile(r'[+=@_!#$%^&*<>?/\|}{~]')
        clean_text = re.sub(special_chars, '', text.strip())
        
        pattern = re.compile(
            r"^(?P<ActivityCode>\d+|[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*)\s+"
            r"(?P<ActivityName>.+?)\s+"
            r"(?:(?P<PercentageComplete>\d+%)\s+)?"
            r"(?:(?P<Duration>\d+\s*d(?:ays?)?|i\s*\d*\s*day|0d|[A-Za-z]+\d*)\s+)?"
            r"(?:"
            r"(?:(?P<StartDay>[A-Za-z]{3})\s+)?"
            r"(?P<StartDate>\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+"
            r"(?:(?P<FinishDay>[A-Za-z]{3})\s+)?"
            r"(?P<FinishDate>\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
            r")?"
            r"(?:\s+(?P<Dependencies>\d+[A-Z]{2}[^0-9]*\d*\s*\w*|\d+)(?:\s*,\s*\d+[A-Z]{2}[^0-9]*\d*\s*\w*|\d+)*)?$",
            re.IGNORECASE
        )
    
        return pattern.match(clean_text)

    def pdf_to_images(self, input_file:str, output_directory:str, image_extension:str="png") -> None:
        pdf = input_file

        if pdf:
            images = convert_from_path(pdf)

            for i, image in enumerate(images):
                image_path = os.path.join(output_directory, f'page_{i + 1}.{image_extension}')
                image.save(image_path, 'PNG')

            print(f"Images saved to: {output_directory}")
        else:
            print("Error: Invalid PDF file.")

    def resize_images(self, image_path:str, image_extension:str="png") -> None:
        image_list = self._bubble_sort_str_list(os.listdir(image_path))

        for i, image in enumerate(image_list):
            image_file = f"{image_path}/{image}"
            
            with Image.open(image_file) as img:
                new_width, new_height = img.width * 2, img.height * 2
                resized_img = img.resize((new_width, new_height))
                
                resized_image_path = f"{image_path}/resized_page_{i+1}.{image_extension}"
                self.sorted_image_list.append(resized_image_path)
                resized_img.save(resized_image_path)
                os.remove(image_file)

        print("Successfully resized images")

    def _bubble_sort_str_list(self, img_dir:list) -> list:
        n = len(img_dir)
        
        for i in range(n):
            swap = False

            for j in range(n - 1 - i):

                img_id = re.search(r'\d+', img_dir[j])
                one_plus_img_id = re.search(r'\d+', img_dir[j + 1])

                img_id = int(img_id.group()) if img_id else 0
                one_plus_img_id = int(one_plus_img_id.group()) if one_plus_img_id else 0

                if img_id > one_plus_img_id:
                    img_dir[j], img_dir[j + 1] = img_dir[j + 1], img_dir[j]
                    swap = True

            if not swap:
                break

        return img_dir

    def process_images(self, image_path:str, roi_msg:str="Select WBS Region", image_extension:str="png") -> None:
        self._select_wbs_region(image_path, roi_msg, image_extension)
        self._repackage_images("package")
        #self._slice_images("slices", image_extension)
        #self._write_txt_file(image_path)
        self._write_json_file(image_path)
        
    def _select_wbs_region(self, image_path:str, roi_msg:str, image_extension:str) -> None:
        if not roi_msg:
            roi_msg = "Select the area"

        if self.sorted_image_list:
            self._crop_images(image_path, roi_msg, image_extension)
            cv.destroyWindow(roi_msg)
        else:
            print("Error: No images found")
        
        print("WBS section successfully defined and images cropped")

    def _repackage_images(self, package_name:str) -> None:
        new_images = []
        for i, image in enumerate(self.sorted_image_list):
            output_path = PdfDataIngestion.repackage_file(image, f"{package_name}_{i+1}")
            new_images.append(output_path)

        self.sorted_image_list.clear()
        self.sorted_image_list = new_images
        print("Images successfully packaged")

    def _crop_images(self, image_path:str, roi_msg:str, image_extension:str) -> None:
        new_images = []
        first_image_path = self.sorted_image_list[0]
        first_image = cv.imread(first_image_path)

        if first_image is None:
            print(f"Error: Could not read image '{first_image_path}'")
            return

        r = cv.selectROI(roi_msg, first_image)

        for i, img_name in enumerate(self.sorted_image_list):
            image = cv.imread(img_name)

            if image is None:
                print(f"Warning: Could not read image '{img_name}' - Skipping.")
                continue

            cropped_image = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

            output_basename = f"cropped_img_{i+1}.{image_extension}"
            output_path = os.path.join(image_path, output_basename)
            
            cv.imwrite(output_path, cropped_image)
            new_images.append(output_path)
            os.remove(img_name)

        self.sorted_image_list.clear()
        self.sorted_image_list = new_images

    def _slice_images(self, new_directory:str, image_extension:str) -> None:
        for image in self.sorted_image_list:
            output_dir = os.path.join(os.path.dirname(image), f"{new_directory}")
            PdfDataIngestion.slice_based_on_color_change(image, output_dir, image_extension)

        print("Images succesfully sliced")

    def detect_vertical_lines(image_path:str, min_line_length:int=100, max_line_gap:int=10) -> list:
        image = cv.imread(image_path)
        if image is None:
            raise ValueError(f"Error: Could not read image '{image_path}'")

        # Convert the image to grayscale
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # Apply edge detection (Canny)
        edges = cv.Canny(gray_image, threshold1=100, threshold2=200)

        # Detect lines using Hough Line Transform
        lines = cv.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=100,
                            minLineLength=min_line_length, maxLineGap=max_line_gap)


        vertical_lines = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if abs(x1 - x2) < 5:  # Ensure the line is approximately vertical
                    vertical_lines.append((x1, y1, x2, y2))

        return vertical_lines

    def _write_txt_file(self, output_path:str, target_directory:str="", file_extension:str="txt", mode:str='a') -> None:
        for package in self.sorted_image_list:
            images_path = os.path.dirname(package) + '/' + target_directory
            sliced_images = self._bubble_sort_str_list(os.listdir(images_path))

            for image in sliced_images:
                image_dir = os.path.join(images_path, image)

                normalized_text = PdfDataIngestion.extract_data_from_image(
                    image_dir, 
                    output_path, 
                    "project_text", 
                    mode
                )
            
            output_file = os.path.join(output_path, f"{target_directory}.{file_extension}")

            with open(output_file, mode) as writer:
                writer.write(normalized_text)
        
        print("Project text file successfully created")

    def _write_json_file(self, output_path:str, target_directory:str="", file_extension:str="json", mode:str='a') -> None:
        project_dict = []
    
        for package in self.sorted_image_list:
            images_path = os.path.dirname(package) + '/' + target_directory
            sliced_images = self._bubble_sort_str_list(os.listdir(images_path))

            for image in sliced_images:
                image_dir = os.path.join(images_path, image)

                normalized_text = PdfDataIngestion.extract_data_from_image(
                    image_dir, 
                    output_path, 
                    "project_text", 
                    mode
                )
                project_dict.append(PdfDataIngestion.jsonify_project_data(normalized_text))
            
        output_file = os.path.join(output_path, f"project_dict.{file_extension}")

        with open(output_file, mode) as file_writer:
            json.dump(project_dict, file_writer)
        
        print("Project json file successfully created")


if __name__ == "__main__":
    PdfDataIngestion.main(False)
