import os
import cv2 as cv
import numpy as np

class ImageProcessing:
    def __init__(self, img_path, proc_img_path):
        self.input_path = img_path    
        self.output_path = proc_img_path

    @staticmethod
    def main():
        project = ImageProcessing.generate_ins()
        project.crop_image(project.input_path)

    @staticmethod
    def generate_ins():
        img_path = input("Enter the image(s) directory to process: ")
        proc_img_path = input("Enter the file directory to save the processed images: ")

        return ImageProcessing(img_path, proc_img_path)

    def crop_image(self, img_path):
        if os.path.isfile(img_path):
            self._crop_single_image(img_path)
        
        elif os.path.isdir(img_path):
            self._crop_multiple_images(img_path)
        
        else:
            print(f"Error: {img_path} is neither a valid file nor a directory.")

    def _crop_single_image(self, img_path):
        image = cv.imread(img_path)
        
        if image is None:
            print(f"Error: Could not read image {img_path}.")
            return

        r = cv.selectROI("Select the area", image)
        cropped_image = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        
        cv.imwrite(self.output_path, cropped_image)
        print(f"Cropped image saved to {self.output_path}")

    def _crop_multiple_images(self, img_dir):
        images = os.listdir(img_dir)

        if not images:
            print(f"Error: No images found in directory {img_dir}.")
            return

        first_image_path = os.path.join(img_dir, images[0])
        first_image = cv.imread(first_image_path)

        if first_image is None:
            print(f"Error: Could not read image {first_image_path}.")
            return

        r = cv.selectROI("Select the area", first_image)

        for i, img_name in enumerate(images):
            img_path = os.path.join(img_dir, img_name)
            image = cv.imread(img_path)

            if image is None:
                print(f"Warning: Could not read image {img_path}. Skipping.")
                continue

            cropped_image = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

            output_file_name = f"cropped_img_{i}.jpg"
            output_path = os.path.join(self.output_path, output_file_name)
            
            cv.imwrite(output_path, cropped_image)


if __name__ == "__main__":
    ImageProcessing.main()