import os
import re
import json
from pdf2image import convert_from_path

class PdfDataIngestion:
    def __init__(self) -> None:
        pass

    @staticmethod
    def main():
        pass

    @staticmethod
    def generate_ins():
        pass

    @staticmethod
    def auto_generate_ins():
        pass

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

    def repackage_files_in_dir(self, input_dir):
        sorted_files = PdfDataIngestion.bubble_sort_str_list(input_dir)

        for i, file in enumerate(sorted_files):
            file_path = os.path.join(input_dir, file)
            PdfDataIngestion.package_file(file_path, f"package_page_{i}")

        print("Files successfully repackaged")


    def pdf_to_images(self, output_directory):
        pdf = self.file_verification()
        if pdf:
            images = convert_from_path(pdf)
            os.makedirs(output_directory, exist_ok=True)

            for i, image in enumerate(images):
                #processed_image = self.process_image(image)

                image_path = os.path.join(output_directory, f'page_{i + 1}.jpg')
                image.save(image_path, 'JPEG')

            print(f"Images saved to: {output_directory}")
        else:
            print("Error: Invalid PDF file.")


if __name__ == "__main__":
    pass