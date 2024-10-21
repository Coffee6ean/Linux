import os
import re
import json
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
from datetime import datetime

class PdfToString():
    def __init__(self, pdf_file_path):
        self.pdf_file_path = pdf_file_path

        pass
    
    @staticmethod
    def ask_user_input():
        file_path_input = input('Please enter the pdf file path to read: ')

        return file_path_input
    
    @staticmethod
    def display_directory_files(list):
        selection_idx = 0
        if len(list)==0:
            print('Error. No files found')
            return -1
        
        if len(list)>1:
            print(f'{len(list)} files found:')
            idx = 0
            for file in list:
                idx += 1
                print(f'{idx}. {file}')

            selection_idx = input('\nPlease enter the index number to select the one to process: ') 
        else:
            print(f'Single file found: {list[0]}')
            print('Will go ahead and process')

        return int(selection_idx) - 1

    @staticmethod
    def is_pdf(file_name):
        if file_name.endswith('.pdf'):
            return True
        else:
            print('Error. Selected file is not a PDF')
            return False

    @staticmethod
    def clear_directory(directory_path):
        if os.path.isdir(directory_path):
            file_list = os.listdir(directory_path)
            for file in file_list:
                file_path = os.path.join(directory_path, file)
                os.remove(file_path)

    def file_verification(self):
        file_path = self.pdf_file_path

        if os.path.isdir(file_path):
            file_list = os.listdir(file_path)
            selection = PdfToString.display_directory_files(file_list)

            file_name = file_list[selection]

            print(f'File selected: {file_name}')
            file = os.path.join(file_path, file_name)
            if PdfToString.is_pdf(file):
                return file
            else:
                return -1
        elif os.path.isfile(file_path):
            if PdfToString.is_pdf(file_path):
                return file_path
            else:
                return -1
        else: 
            print('Error. Please verify the directory and file exist and that the file is of type .pdf')    
            return -1
        
    def read_pdf_file(self):
        pdf = self.file_verification()
        if PdfToString.is_pdf(pdf):
            reader = PdfReader(pdf)
            first_page = reader.pages[0]
            content_str = first_page.extract_text()
            print('#-------------#')
            print(content_str)

    def pdf_to_img(self, output_directory):
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
    
    def process_image(self, image):
        image = image.convert('L')
        image = image.filter(ImageFilter.MedianFilter(size=3))

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)
        threshold = 128
        image = image.point(lambda p: 255 if p > threshold else 0)

        return image

    def read_pdf_img(self, input_directory):
        img_path = os.path.join(input_directory, "page_1.jpg")
        image = Image.open(img_path)
        process_img = self.process_image(image)
        text = pytesseract.image_to_string(process_img)
        print('#-------------#')
        print(text)


if __name__ == "__main__":
    temp_imgs_path = '/home/coffee_6ean/Linux/CriticalFlowPath/src/local_results/images'
    file_path_input = PdfToString.ask_user_input()

    new_pdf_str = PdfToString(file_path_input)
    #new_pdf_str.read_pdf_file()
    new_pdf_str.pdf_to_img(temp_imgs_path)
    #new_pdf_str.read_pdf_img(temp_imgs_path)

    print(f'Process completed successfully. Would you like to clear the contents of the temporary images directory: {temp_imgs_path}')
    clear_directory = input('Enter "Y/y" to clear the directory or "N/n" to keep the contents: ')
    if clear_directory.lower() == "y":
        PdfToString.clear_directory(temp_imgs_path)
        