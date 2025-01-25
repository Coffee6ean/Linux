import os
import re
import json
from datetime import datetime
import modules as mdls

import sys
sys.path.append("../")
from CriticalFlowPath.keys.secrets import RSLTS_DIR

class App:
    #Structures
    file_management = {
            "create": ["create", "c"],
            "read": ["read", "r"],
            "update": ["update", "u"],
            "delete": ["delete", "d"],
        }
    allowed_extensions = ["xlsx", "xml"]

    def __init__(self, project_ins_dict):
        self.obj = project_ins_dict
        self.schedule_worksheet = "CFA - Schedule"
        self.legends_worksheet = "CFA - Legends"

    @staticmethod
    def main(auto=True):
        project = App.generate_ins()

        if project:
            project.execute_project_package()

    @staticmethod
    def generate_ins() -> dict:
        App.ynq_user_interaction(
            "Is this a completly new project? "
        )

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

    def create_project_folder(self) -> None:
        results_folder = RSLTS_DIR
        client_folder = self.obj["project"]["metadata"].get("client")
        date_folder = self.obj["project"]["metadata"]["dates"].get("created")

        project_path = os.path.join(results_folder, client_folder, date_folder)
        os.makedirs(project_path, exist_ok=True)

        return project_path

    def execute_project_package(self, auto:bool=True) -> None:
        ins_obj = self.obj["setup"]
        mdl_1 = ins_obj["project"]["modules"].get("MODULE_1")
        mdl_2 = ins_obj["project"]["modules"].get("MODULE_2")

        self._print_result("WbsFramework processing...")
        mdls.WbsFramework.main(
            auto, 
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"),
            self.schedule_worksheet,
            mdl_2["content"].get("table"),
            mdl_2["content"].get("custom_ordered_dict"),
        )

        self._print_result("ScheduleFramework processing...")
        mdls.ScheduleFramework.main(
            auto,
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"), 
            self.schedule_worksheet,
            mdl_2["content"].get("table"),
            mdl_2["content"].get("custom_ordered_dict"),
            mdl_2["content"].get("custom_phase_order"),
            mdl_2["content"].get("lead_schedule_struct"),
            mdl_1["details"].get("start_date"),
            mdl_1["details"].get("finish_date"),
        )

        self._print_result("PostProcessingFramework processing...")
        mdls.PostProcessingFramework.main(
            auto,
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"), 
            self.schedule_worksheet,
            mdl_2["content"].get("table"),
            mdl_2["content"].get("custom_ordered_dict"),
            mdl_2["content"].get("custom_phase_order"),
            mdl_2["content"].get("lead_schedule_struct"),
            mdl_1["details"].get("start_date"),
            mdl_1["details"].get("finish_date"),
        )

        self._print_result("LegendsFramework processing...")
        mdls.LegendsFramework.main(
            auto,
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"), 
            self.legends_worksheet,
            mdl_2["content"].get("table"),
        )
        
        # == WIP == #
        """ self._print_result("DataRelationship processing...")
        mdls.DataRelationship.main(auto, self.obj) """

    def _print_result(self, prompt_message:str) -> None:
        print()
        print()
        print(f'//========== {prompt_message} ==========//')
        print()


if __name__ == "__main__":
    App.main(False)
