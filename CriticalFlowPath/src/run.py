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
        self.schedule_worksheet_macro = "Macro CFA - Schedule"
        self.activity_list_worksheet = "CFA - Activity List"
        self.legends_worksheet = "CFA - Legends"

        #Structures
        self.project_documentation_title = "ticket.json"
        self.folder_structure = ["client", "name", "date"]

    @staticmethod
    def main(auto:bool, payload:dict):
        project = App.generate_ins(auto, payload)

        if project:
            #Generate Project Folder
            project_folder = App.create_project_folder(project.obj["setup"], RSLTS_DIR)

            #Process and Document File
            project.execute_project_package(project_folder)
            project.document_project_package(project_folder)

            #Sort and Order File
            App.move_project_to_folder(project.obj["setup"], project_folder)

    @staticmethod
    def generate_ins(auto:bool, payload:dict) -> dict:
        if not payload:
            App.ynq_user_interaction(
                "Is this a completly new project? "
            )

        setup = mdls.Setup.main(auto, payload)

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
        entry_date = project_ins["project"]["metadata"]["dates"].get("created")
        entry_month = datetime.strptime(entry_date, "%d-%b-%y %H:%M:%S").month
        
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
                    new_directory += calendar_months[entry_month] + '/' + entry_date
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

    @staticmethod
    def write_data_to_json(file_title:str, json_dict:dict):
        file = os.path.join(RSLTS_DIR, file_title)
        
        with open(file, 'w') as writer:
            json.dump(json_dict, writer)

    def execute_project_package(self, project_folder:str, auto:bool=True) -> None:
        ins_obj = self.obj["setup"]
        mdl_1 = ins_obj["project"]["modules"].get("MODULE_1")
        mdl_2 = ins_obj["project"]["modules"].get("MODULE_2")
        mdl_3 = ins_obj["project"]["modules"].get("MODULE_3")

        self._print_result("WbsFramework (CFA) processing...")
        mdls.WbsFramework.main(
            auto, 
            True,
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"),
            self.schedule_worksheet,
            mdl_2["content"].get("table"),
            mdl_2["content"].get("custom_ordered_dict"),
        )

        self._print_result("ScheduleFramework (CFA) processing...")
        mdls.ScheduleFramework.main(
            auto,
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"), 
            mdl_3["details"].get("workweek"), 
            self.schedule_worksheet,
            mdl_2["content"].get("table"),
            mdl_3.get("content"),
            mdl_2["content"].get("custom_phase_order"),
            mdl_2["content"].get("lead_schedule_struct"),
            mdl_1["details"].get("start_date"),
            mdl_1["details"].get("finish_date"),
            'd',
        )

        self._print_result("PostProcessingFramework (CFA) processing...")
        mdls.PostProcessingFramework.main(
            auto,
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"),
            mdl_3["details"].get("workweek"), 
            self.schedule_worksheet,
            mdl_2["content"].get("table"),
            mdl_3.get("content"),
            mdl_2["content"].get("custom_phase_order"),
            mdl_2["content"].get("lead_schedule_struct"),
            mdl_3["details"]["calendar"]["processed"]["days"].get("total"),
            mdl_1["details"].get("start_date"),
            mdl_1["details"].get("finish_date"),
            'd',
        )

        self._print_result("WbsFramework (Macro CFA) processing...")
        mdls.WbsFramework.main(
            auto, 
            True,
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"),
            self.schedule_worksheet_macro,
            mdl_2["content"].get("table"),
            mdl_2["content"].get("custom_ordered_dict"),
        )

        self._print_result("ScheduleFramework (Macro CFA) processing...")
        mdls.ScheduleFramework.main(
            auto,
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"), 
            mdl_3["details"].get("workweek"), 
            self.schedule_worksheet_macro,
            mdl_2["content"].get("table"),
            mdl_3.get("content"),
            mdl_2["content"].get("custom_phase_order"),
            mdl_2["content"].get("lead_schedule_struct"),
            mdl_1["details"].get("start_date"),
            mdl_1["details"].get("finish_date"),
            'w',
        )

        self._print_result("PostProcessingFramework (Macro CFA) processing...")
        mdls.PostProcessingFramework.main(
            auto,
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"),
            mdl_3["details"].get("workweek"), 
            self.schedule_worksheet_macro,
            mdl_2["content"].get("table"),
            mdl_3.get("content"),
            mdl_2["content"].get("custom_phase_order"),
            mdl_2["content"].get("lead_schedule_struct"),
            mdl_3["details"]["calendar"]["processed"]["days"].get("total"),
            mdl_1["details"].get("start_date"),
            mdl_1["details"].get("finish_date"),
            'w',
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
        
        self._print_result("AnalyticsFramework processing...")
        mdls.AnalyticsFramework.main(
            auto,
            ins_obj["input_file"].get("path"), 
            ins_obj["input_file"].get("basename"),
            ins_obj["input_file"].get("extension"),
            project_folder,
            mdl_2["content"].get("table"),
            mdl_2["content"].get("lead_schedule_struct"),
        )

    def document_project_package(self, project_folder:str) -> None:
        ins_obj = self.obj["setup"]
        mdl_1 = ins_obj["project"]["modules"].get("MODULE_1")
        mdl_2 = ins_obj["project"]["modules"].get("MODULE_2")
        mdl_3 = ins_obj["project"]["modules"].get("MODULE_3")
        
        ins_obj["project"]["metadata"]["dates"]["finished"] = App.return_valid_date()
        
        ticket_body = {
            "metadata": ins_obj["project"].get("metadata"),
            "data": mdl_1.get("content"),
            "details": {
                "MDL_1": mdl_1.get("details"),
                "MDL_2": mdl_2.get("details"),
                "MDL_3": mdl_3.get("details"),
            },
            "logs": {
                "MDL_1": mdl_1.get("logs"),
                "MDL_2": mdl_2.get("logs"),
                "MDL_3": mdl_3.get("logs"),
            },
            "status": None,
        }

        basename = self.project_documentation_title
        file = os.path.join(project_folder, basename)

        with open(file, 'w') as writer:
            json.dump(ticket_body, writer)

    def _print_result(self, prompt_message:str) -> None:
        print()
        print()
        print(f'//========== {prompt_message} ==========//')
        print()


if __name__ == "__main__":
    App.main(True, {})
