import os

import sys
sys.path.append("../")
from FileAnalyst.config.paths import RSLTS_DIR
import modules as mdls

class App:
    allowed_file_types = ["pdf", "txt"]

    def __init__(self, proc_as_img, input_file_path, input_file_basename, 
                 input_file_extension, target_words_list) -> None:
        self.img_proc = proc_as_img
        self.input_path = input_file_path
        self.input_basename = input_file_basename
        self.input_extension = input_file_extension
        self.input_words_list = target_words_list

    @staticmethod
    def main(auto, input_file_path=None, input_file_basename=None, input_file_extension=None, 
             target_words_list=[]):
        if auto:
            project = App.auto_generate_ins(
                input_file_path, 
                input_file_basename, 
                input_file_extension, 
                target_words_list
            )
        else:
            project = App.generate_ins()

        if project:
            mdls.setup.Setup.main(True, project)

    @staticmethod
    def generate_ins():
        input_file = App.return_valid_file(
            input("Please enter the path to the file or directory: ").strip()
        )

        if input_file:
            input_style_process = App.binary_user_interaction("Would you like to process file as images? [Y/N]: ")
            input_target_words = [item.strip() for item in input("Please enter the target words/phrases (comma-separated): ").split(',')]

            ins = App(
                input_style_process,
                input_file.get("path"), 
                input_file.get("basename"), 
                input_file.get("extension"),
                input_target_words
            )

            return ins

    @staticmethod
    def auto_generate_ins(input_file_path=None, input_file_basename=None,
                          input_file_extension=None, target_words_list=[]):
        ins = App(
            input_file_path, 
            input_file_basename, 
            input_file_extension, 
            target_words_list
        )

        return ins

    @staticmethod
    def return_valid_file(input_file_dir:str) -> dict|int:
        if not os.path.exists(input_file_dir):
            raise FileNotFoundError("Error: Given directory or file does not exist in the system.")

        if os.path.isdir(input_file_dir):
            file_dict = App._handle_dir(input_file_dir)
        elif os.path.isfile(input_file_dir):
            file_dict = App._handle_file(input_file_dir)

        return file_dict
    
    @staticmethod
    def _handle_dir(input_file_dir:str, mode:str="r") -> dict|int:
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_file_dir)
            selection = App._display_directory_files(dir_list)
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
                selection_idx = int(input('\nPlease enter the index number to select the one to process. If you dont find your option enter "-1" to continue: '))
                if selection_idx == -1:
                    return selection_idx
                
                if 1 <= selection_idx <= len(file_list):  
                    return selection_idx - 1  
                else:
                    print(f'Error: Please enter a number between 1 and {len(file_list)}.')
            except ValueError:
                print('Error: Invalid input. Please enter a valid number.\n')

    @staticmethod
    def _handle_file(input_file_dir:str) -> dict:
        input_file_extension = os.path.basename(input_file_dir).split(".")[-1]

        if (input_file_extension in App.allowed_file_types):
            return dict(
                path = os.path.dirname(input_file_dir), 
                basename = os.path.basename(input_file_dir).split(".")[0],
                extension = input_file_extension,
            )

        print("Error: Please verify that the directory and file exist and that the file extension complies with class attributes")
        return {}

    @staticmethod
    def binary_user_interaction(prompt_message:str) -> bool:
        valid_responses = {'y', 'n'}  
        
        while True:
            user_input = input(prompt_message).lower().strip()
            
            if user_input in valid_responses:
                if user_input == 'y':
                    return True 
                else:
                    return False 
            else:
                print("Error. Invalid input, please try again. ['Y/y' for Yes, 'N/n' for No]\n")


if __name__ == "__main__":
    App.main(False)
