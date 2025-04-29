import os
import re
import json
from datetime import datetime
import modules as mdls

import sys
sys.path.append("../")
from CpmProcessor.keys.secrets import RSLTS_DIR

class App:
    #Structures
    file_management = [
        "CREATE",
        "READ",
        "UPDATE",
        "DELETE",
    ]
    allowed_extensions = ["xlsx", "xml"]

    def __init__(self, project_ins_dict):
        self.obj = project_ins_dict
        self.cross_reference_table = "Referenced - WBS Table"
        self.wbs_table = "Compared - WBS Table"

        #Structures
        self.project_documentation_title = "ticket.json"
        self.folder_structure = ["client", "name", "date"]

    @staticmethod
    def main():
        project = App.generate_ins()

        if project:
            project_folder = App.create_project_folder(project.obj["setup"], RSLTS_DIR)

            project.execute_project_package()
            project.document_project_package(project_folder)

            App.move_project_to_folder(project.obj["setup"], project_folder)

    @staticmethod
    def generate_ins() -> dict:
        print("== Initializing 'CpmProcessor' tool ==")

        setup = mdls.Setup.main()

        project_ins_dict = {"setup": setup.obj}
        ins = App(project_ins_dict)

        return ins

    @staticmethod
    def ynq_user_interaction(prompt_message):
        valid_responses = {'y', 'n', 'q'}  
        
        while True:
            user_input = input(prompt_message).lower().strip()
            
            if user_input in valid_responses:
                return user_input  
            else:
                print("Error. Invalid input, please try again. ['Y/y' for Yes, 'N/n' for No, 'Q/q' for Quit]\n")

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
                selection_idx = int(input('\nPlease enter the index number to select the one to process: '))
                if 1 <= selection_idx <= len(file_list):  
                    return selection_idx - 1  
                else:
                    print(f'Error: Please enter a number between 1 and {len(file_list)}.')
            except ValueError:
                print('Error: Invalid input. Please enter a valid number.\n')

    @staticmethod
    def _handle_file(input_file_dir:str):
        input_file_extension = os.path.basename(input_file_dir).split(".")[-1]

        if (input_file_extension in App.allowed_extensions):
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
    def normalize_entry(entry_str:str) -> str:
        special_chars = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        remove_special_chars = re.sub(special_chars, '', entry_str.lower())
        normalized_str = re.sub(' ', '_', remove_special_chars)

        return normalized_str

    @staticmethod
    def create_project_folder(project_ins:dict, parent_dir:str) -> None:
        folder_structure = ["client", "name", "date"]
        entry_date = datetime.now()
        entry_month = datetime.now().month
        
        calendar_months = {
            1:"Jan",
            2:"Feb",
            3:"Mar",
            4:"Apr",
            5:"May",
            6:"Jun",
            7:"Jul",
            8:"Aug",
            9:"Sep",
            10:"Oct",
            11:"Nov",
            12:"Dec",
        }

        def create_dir(directory_name:str, counter:int=0, new_directory:str=""):
            if counter == len(folder_structure):
                os.makedirs(directory_name, exist_ok=True)
                return directory_name
            else:
                category = folder_structure[counter]

                if category == "date": 
                    new_directory += calendar_months[entry_month] + '/' + datetime.strftime(entry_date, "%d-%b-%y %H:%M:%S")
                else:
                    new_directory += project_ins["project"]["metadata"].get(category) + '/'

                new_folder_dir = os.path.join(directory_name, new_directory)
                return create_dir(new_folder_dir, counter + 1)

        folder = create_dir(parent_dir)
        return folder
    
    @staticmethod
    def move_project_to_folder(project_ins:dict, parent_dir:str) -> None:
        input_path = project_ins["input_file"].get("path")
        input_basename = project_ins["input_file"].get("basename")
        input_extension = project_ins["input_file"].get("extension")
        basename = input_basename + '.' + input_extension
        
        init_dir = os.path.join(input_path, basename)
        final_dir = os.path.join(parent_dir, basename)

        os.rename(init_dir, final_dir)
                        
    def execute_project_package(self, db_action:str=None, project_folder:str=None, auto:bool=True) -> None:
        ins_obj = self.obj["setup"]
        mdl_2 = ins_obj["project"]["modules"].get("MODULE_2")
        mdl_3 = ins_obj["project"]["modules"].get("MODULE_3")

        self._print_result("TableFramework processing...")
        mdls.TableFramework.main(
            auto, 
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"),
            self.cross_reference_table,
            mdl_2["content"].get("referenced")
        )

        self._print_result("WBSFramework processing...")
        mdls.WbsFramework.main(
            auto, 
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"),
            self.wbs_table,
            mdl_3["content"].get("compared")
        )

    def document_project_package(self, project_folder:str) -> None:
        ins_obj = self.obj["setup"]

        ticket_body = {
            "metadata": ins_obj["project"].get("metadata"),
            "data": self._get_last_module_data(ins_obj["project"]["modules"]),
            "details": {key: value.get("details") for key, value in ins_obj["project"]["modules"].items()},
            "logs": {key: value.get("logs") for key, value in ins_obj["project"]["modules"].items()},
            "status": None,
        }

        basename = self.project_documentation_title
        file = os.path.join(project_folder, basename)

        with open(file, 'w') as writer:
            json.dump(ticket_body, writer)

    def _get_last_module_data(self, project_dict:dict):
        last_module_key = list(project_dict.keys())[-1]
        last_module = project_dict.get(last_module_key)

        return last_module

    def _print_result(self, prompt_message:str) -> None:
        print()
        print()
        print(f'//========== {prompt_message} ==========//')
        print()


if __name__ == "__main__":
    App.main()
