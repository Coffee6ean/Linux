import os
import re
import json
import copy
import argparse
from datetime import datetime

import sys
sys.path.append("../")
from backend.src import modules as mdls
from backend.config.paths import RSLTS_DIR

class App:
    #Structures
    file_management = {
        "create": ["create", "c"],
        "read": ["read", "r"],
        "update": ["update", "u"],
        "delete": ["delete", "d"],
    }
    allowed_extensions = ["xlsx", "xml"]
    project_folder_structure = ["client", "name", "date"]

    ticket = {
        "metadata": {},
        "data": {},
        "setup": {},
        "process":{}
    }

    def __init__(self, project_ins_dict):
        self.obj = project_ins_dict
        self.schedule_worksheet = "CFA - Schedule"
        self.schedule_worksheet_macro = "Macro CFA - Schedule"
        self.activity_list_worksheet = "CFA - Activity List"
        self.legends_worksheet = "CFA - Legends"

        #Structures
        self.project_documentation_title = "ticket.json"

    @staticmethod
    def main(payload:dict):
        project = App.generate_ins(payload)

        if project:
            #Generate Project Folder
            project_folder = App.create_project_folder(project.obj["setup"], RSLTS_DIR)

            #Process Project File
            App.execute_full_project_framework(project, project_folder)

            #Sort and Order Project File
            App.move_project_to_folder(
                project.obj["setup"], 
                project_folder, 
                project.obj["setup"]["input_file"].get("basename")
            )

            #Document Project File
            App.document_project_package(project, project_folder, App.ticket)

            return project.obj

    @staticmethod
    def generate_ins(payload:dict) -> dict:
        if not payload:
            App.ynq_user_interaction(
                "Is this a completly new project? "
            )

        setup = mdls.Setup.main(payload)

        project_ins_dict = {"setup": setup.obj}
        App.clean_and_store_ticket_section(
            project_ins_dict, 
            "setup", 
            "content", 
            ["project","modules"], 
            True
        )

        ins = App(project_ins_dict)

        return ins

    @staticmethod
    def ynq_user_interaction(prompt_message:str) -> str:
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
        special_chars = re.compile('[@_!#$%^&*()<>?/\\|}{~:]')
        remove_special_chars = re.sub(special_chars, '', entry_str.lower())
        normalized_str = re.sub(' ', '_', remove_special_chars)

        return normalized_str

    @staticmethod
    def create_project_folder(project_ins: dict, parent_dir: str) -> str:
        entry_date = project_ins["project"]["metadata"]["dates"].get("created")
        entry_month = datetime.strptime(entry_date, "%d-%b-%y %H:%M:%S").month

        calendar_months = {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
        }

        def create_dir(directory_name: str, counter: int = 0) -> str:
            if counter == len(App.project_folder_structure):
                os.makedirs(directory_name, exist_ok=True)
                return directory_name
            else:
                category = App.project_folder_structure[counter]

                if category == "date":
                    # append month and date as folders
                    new_directory = os.path.join(directory_name, calendar_months[entry_month], entry_date)
                else:
                    # append the metadata category folder
                    folder_name = project_ins["project"]["metadata"].get(category)
                    if folder_name is None:
                        folder_name = "Unknown"
                    new_directory = os.path.join(directory_name, folder_name)

                return create_dir(new_directory, counter + 1)

        folder = create_dir(parent_dir)
        return folder

    @staticmethod
    def write_data_to_json(file_title:str, json_dict:dict) -> None:
        file = os.path.join(RSLTS_DIR, file_title)
        
        with open(file, 'w') as writer:
            json.dump(json_dict, writer)

    @staticmethod
    def execute_full_project_framework(project_ins, project_folder:str, auto:bool=True) -> None:
        setup = project_ins.obj["setup"]
        modules = setup["project"]["modules"]

        # Extract key modules
        mdl_1 = modules.get("MODULE_1")
        mdl_2 = modules.get("MODULE_2")
        mdl_3 = modules.get("MODULE_3")

        # Run CFA frameworks 
        App.run_cfa_pipeline(
            "CFA", 
            True,
            setup["input_file"].get("path"),
            setup["input_file"].get("basename"),
            setup["input_file"].get("extension"),
            project_ins.schedule_worksheet, 
            mdl_3["details"].get("workweek"),
            mdl_2["content"].get("table"), 
            mdl_3.get("content"),
            mdl_2["content"].get("custom_phase_order"),
            mdl_2["content"].get("lead_schedule_struct"),
            mdl_3["details"]["calendar"]["processed"]["days"].get("total"),
            mdl_1["details"].get("start_date"),
            mdl_1["details"].get("finish_date"),
            'd',
            auto
        )
        App.run_cfa_pipeline(
            "Macro CFA", 
            True,
            setup["input_file"].get("path"),
            setup["input_file"].get("basename"),
            setup["input_file"].get("extension"),
            project_ins.schedule_worksheet_macro,
            mdl_3["details"].get("workweek"),
            mdl_2["content"].get("table"), 
            mdl_3.get("content"),
            mdl_2["content"].get("custom_phase_order"),
            mdl_2["content"].get("lead_schedule_struct"),
            mdl_3["details"]["calendar"]["processed"]["days"].get("total"),
            mdl_1["details"].get("start_date"),
            mdl_1["details"].get("finish_date"),
            'w',
            auto
        )

        App.ticket["metadata"] = setup["project"].get("metadata")
        App.ticket["data"] = mdl_3.get("content")

        # Legends Framework
        App.run_legends_pipeline(
            setup["input_file"].get("path"),
            setup["input_file"].get("basename"),
            setup["input_file"].get("extension"),
            project_ins.legends_worksheet,
            mdl_2["content"].get("table"),
            auto
        )

        # Analytics Framework
        App.run_analytics_pipeline(
            setup["input_file"].get("path"),
            setup["input_file"].get("basename"),
            setup["input_file"].get("extension"),
            project_folder,
            mdl_2["content"].get("table"),
            mdl_2["content"].get("lead_schedule_struct"),
            auto
        )

    @staticmethod
    def run_cfa_pipeline(header_title:str, is_framed:bool,
                         project_path:str, project_basename:str, project_extension:str,
                         project_worksheet:str, project_workweek:str, project_table, 
                         project_dictionary:dict, project_phase_order, project_lead_struct, 
                         project_duration, project_start_date:str, project_finish_date:str, 
                         project_time_scale:str='d', auto:bool=True) -> None:
        App._print_result(f"WbsFramework ({header_title}) processing...")
        mdl_1 = mdls.WbsFramework.main(
            auto,
            is_framed,
            project_path,
            project_basename,
            project_extension,
            project_worksheet,
            project_table,
            project_dictionary
        )
        App.ticket["process"].setdefault("WbsFramework", mdl_1) 

        App._print_result(f"ScheduleFramework ({header_title}) processing...")
        mdl_2 = mdls.ScheduleFramework.main(
            auto,
            project_path,
            project_basename,
            project_extension,
            project_workweek,
            project_worksheet,
            project_table,
            project_dictionary,
            project_phase_order,
            project_lead_struct,
            project_start_date,
            project_finish_date,
            project_time_scale
        )
        App.ticket["process"].setdefault("ScheduleFramework", mdl_2) 

        App._print_result(f"PostProcessingFramework ({header_title}) processing...")
        mdl_3 = mdls.PostProcessingFramework.main(
            auto,
            project_path,
            project_basename,
            project_extension,
            project_workweek,
            project_worksheet,
            project_table,
            project_dictionary,
            project_phase_order,
            project_lead_struct,
            project_duration,
            project_start_date,
            project_finish_date,
            project_time_scale
        )
        App.ticket["process"].setdefault("PostProcessingFramework", mdl_3) 

    @staticmethod
    def run_legends_pipeline(project_path, project_basename, project_extension, 
                             project_worksheet, project_table, auto:bool=True) -> None:
        App._print_result("LegendsFramework processing...")
        lgnds = mdls.LegendsFramework.main(
            auto,
            project_path,
            project_basename,
            project_extension,
            project_worksheet,
            project_table
        )
        App.ticket["process"].setdefault("LegendsFramework", lgnds) 

    @staticmethod
    def run_analytics_pipeline(project_path, project_basename, project_extension, 
                               project_folder, project_table, project_lead_struct, auto:bool=True):
        App._print_result("AnalyticsFramework processing...")
        nlytcs = mdls.AnalyticsFramework.main(
            auto,
            project_path,
            project_basename,
            project_extension,
            project_folder,
            project_table,
            project_lead_struct
        )
        App.ticket["process"].setdefault("AnalyticsFramework", nlytcs) 

    @staticmethod
    def move_project_to_folder(project_ins:dict, project_file_path:str, project_file_basename:str) -> None:
        App.ticket["setup"]["output_file"]["path"] = project_file_path
        App.ticket["setup"]["output_file"]["basename"] = project_file_basename
        
        input_path = project_ins["input_file"].get("path")
        input_basename = project_ins["input_file"].get("basename")
        input_extension = project_ins["input_file"].get("extension")
        basename = input_basename + '.' + input_extension
        
        init_dir = os.path.join(input_path, basename)
        final_dir = os.path.join(project_file_path, basename)

        os.rename(init_dir, final_dir)

    @staticmethod
    def document_project_package(project_ins, project_folder:str, ticket_dict:dict) -> None:
        basename = project_ins.project_documentation_title
        file = os.path.join(project_folder, basename)

        with open(file, 'w') as writer:
            json.dump(ticket_dict, writer)

    @staticmethod
    def _print_result(prompt_message:str) -> None:
        print()
        print()
        print(f'//========== {prompt_message} ==========//')
        print()

    @staticmethod
    def clean_and_store_ticket_section(source_dict:dict, parent_key:str, target_key:str, 
                                     target_path:list, remove_all:bool=True) -> None:
        ticket_copy = copy.deepcopy(source_dict)
        target_section = App._navigate_to_path(ticket_copy[parent_key], target_path)

        cleaned_section = App.clear_key_from_dictionary(target_section, target_key, remove_all)
        ticket_section_replaced = App._replace_at_path(ticket_copy, cleaned_section, ["setup", "project"])
 
        App.ticket[parent_key] = ticket_section_replaced

    @staticmethod
    def _check_dictionary_for_json_serializable(json_dict:dict) -> bool:
        try:
            json.dumps(json_dict)
            return True
        except (TypeError, OverflowError):
            return False

    @staticmethod
    def clear_key_from_dictionary(json_dict:dict, target_key:str, multiple:bool) -> dict|None:
        def traverse_dict_single(obj:dict|list, target_key:str) -> dict|list:
            if isinstance(obj, dict):
                if target_key in obj:
                    obj.pop(target_key)
                    return obj
                for value in obj.values():
                    result = traverse_dict_single(value, target_key)
                    if result is not None:
                        return obj
            elif isinstance(obj, list):
                for item in obj:
                    result = traverse_dict_single(item, target_key)
                    if result is not None:
                        return obj
            return None

        def traverse_dict_multiple(obj:dict|list, target_key:str) -> dict|list:
            if isinstance(obj, dict):
                obj.pop(target_key, None)
                for value in obj.values():
                    traverse_dict_multiple(value, target_key)
            elif isinstance(obj, list):
                for item in obj:
                    traverse_dict_multiple(item, target_key)
            return obj

        if multiple:
            traverse_dict_multiple(json_dict, target_key)
        else:
            traverse_dict_single(json_dict, target_key)

        return json_dict

    @staticmethod
    def _navigate_to_path(json_dict:dict, target_path:list) -> dict:
        if not target_path:
            return json_dict

        key = target_path.pop(0)

        if not isinstance(json_dict, dict) or key not in json_dict:
            print(f"Key '{key}' not found.")
            return None

        return App._navigate_to_path(json_dict[key], target_path)
    
    @staticmethod
    def _replace_at_path(json_dict:dict, replace_dict:dict, target_path:list) -> dict|None:
        if not target_path:
            print("Error: Empty target path; nothing to replace.")
            return None

        key = target_path[0]
        if len(target_path) == 1:
            json_dict[key] = replace_dict
            return json_dict

        if key not in json_dict or not isinstance(json_dict[key], dict):
            print(f"Key '{key}' not found or not a dict.")
            return None

        return App._replace_at_path(json_dict[key], replace_dict, target_path[1:])


if __name__ == "__main__":
    """ parser = argparse.ArgumentParser()
    parser.add_argument("--auto", action="store_true", help="Run without prompts")
    args = parser.parse_args() """

    App.main({})
