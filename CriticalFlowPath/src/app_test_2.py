import os
import re
import json

import sys
sys.path.append("../")
from CriticalFlowPath.keys.secrets import RSLTS_DIR

from datetime import datetime
import modules as mdls


class App:
    #Structures
    file_management = {
            "create": ["create", "c"],
            "read": ["read", "r"],
            "update": ["update", "u"],
            "delete": ["delete", "d"],
        }
    allowed_extensions = ["xlsx", "xml"]

    def __init__(self, project_ins_dict:dict):
        self.ins = project_ins_dict

    @staticmethod
    def main(auto=True):
        if auto:
            project = App.auto_generate_ins()
        else:
            project = App.generate_ins()

        if project:
            project.ins["output_file"]["folder"] = project.create_project_folder()
            project.execute_project_package()

    @staticmethod
    def generate_ins() -> dict:
        process_continuity = input("Is this a completly new project? ")
        if process_continuity == 'q':
            print("Exiting the program.")
            return -1
        
        input_file_dir = App.return_valid_file(
            input("Please enter the path to the file or directory to read: ").strip()
        )
        output_file_dir = App.return_valid_path(
            "Please enter the directory to save the new package results: "
        )
        input_project_code = input("Enter Project Code: ").strip()
        input_project_title = input("Enter Project Title: ").strip()
        input_project_subtitle = input("Enter Project Subtitle: ").strip()
        input_project_client = input("Enter Project Client: ").strip()

        project_ins_dict = {
            "input_file": dict(
                path = input_file_dir.get("path"),
                basename = input_file_dir.get("basename"),
                extension = input_file_dir.get("extension"),
            ),
            "output_file": dict(
                parent_folder = output_file_dir,
                folder = None,
                files = {},
            ),
            "project": dict(
                metadata = dict(
                    id = None,
                    continuity = process_continuity,
                    dates = dict(
                        created = App.return_valid_date(),
                        updated = [(App.__name__, App.return_valid_date())],
                    ),
                    code = input_project_code,
                    title = input_project_title,
                    subtitle = input_project_subtitle,
                    client = input_project_client,
                ),
                data = {},
            ),
        }

        ins = App(project_ins_dict)
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

    def create_project_folder(self) -> None:
        results_folder = RSLTS_DIR
        client_folder = self.ins["project"]["metadata"].get("client")
        date_folder = self.ins["project"]["metadata"]["dates"].get("created")

        project_path = os.path.join(results_folder, client_folder, date_folder)
        os.makedirs(project_path, exist_ok=True)

        return project_path

    def execute_project_package(self, auto:bool=True) -> None:
        self._print_result("DataIngestion processing...")
        mdl_data_1 = mdls.DataIngestion.main(
            auto, 
            self.ins["input_file"].get("path"), 
            self.ins["input_file"].get("basename"),
            self.ins["input_file"].get("extension"),
            self.ins["output_file"].get("parent_folder"),
            self.ins["project"]["metadata"].get("code"),
            self.ins["project"]["metadata"].get("title"),
            self.ins["project"]["metadata"].get("sibtitle"),
            self.ins["project"]["metadata"].get("client"),
            self.ins["project"]["metadata"]["dates"].get("created")
        )
        print(mdl_data_1)
        self.ins["project"]["data"] = {
            mdls.DataIngestion.__name__: mdl_data_1
        }

        print(self.ins)

        """ self._print_result("WbsFramework processing...")
        project_wbs = mdls.WbsFramework.main(
            auto, 
            self.ins["project_continuity"], 
            self.ins["r_xlsx_file"], 
            self.ins["w_xlsx_ws"], 
            self.ins["w_json_file"], 
            self.ins["json_title"]
        )
        
        self._print_result("ScheduleFramework processing...")
        project_schdl = mdls.ScheduleFramework.main(
            auto, 
            self.ins["r_xlsx_file"], 
            self.ins["w_json_file"], 
            self.ins["w_xlsx_ws"], 
            project_data["project_start_date"], 
            project_data["project_finish_date"], 
            self.ins["json_title"]
        )
        
        # == WIP == #
        self._print_result("DataRelationship processing...")
        mdls.DataRelationship.main(auto, self.ins)

        self._print_result("LegendsFramework processing...")
        project_lgnds = mdls.LegendsFramework.main(
            auto, 
            self.ins["r_xlsx_file"], 
            self.ins["ws_legends"], 
            self.ins["w_json_file"], 
            self.ins["json_title"]
        )
            
        self._print_result("ExcelPostProcessing processing...")
        project_post = mdls.ExcelPostProcessing.main(
            auto, 
            self.ins["r_xlsx_file"], 
            self.ins["w_xlsx_ws"], 
            project_data["project_start_date"], 
            project_data["project_finish_date"],  
            self.ins["w_json_file"], 
            self.ins["json_title"]
        ) """

    def _print_result(self, prompt_message:str) -> None:
        print()
        print()
        print(f'//========== {prompt_message} ==========//')
        print()

if __name__ == "__main__":
    App.main(False)
