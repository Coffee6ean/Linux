import os
import json
from datetime import datetime

# Imported Helper - As Package 
from modules.utils.xlsx.data_ingestion import XlsxDataIngestion
from modules.utils.xlsx.data_referencing import XlsxDataReferencing
from modules.utils.xlsx.data_comparing import XlsxDataComparing

# Imported Helper - As Module
""" from utils.xlsx.data_ingestion import XlsxDataIngestion
from utils.xlsx.data_referencing import XlsxDataReferencing
from utils.xlsx.data_comparing import XlsxDataComparing
 """

import sys
sys.path.append("../")
from CpmProcessor.keys.secrets import RSLTS_DIR

from CpmProcessor.src import db

class Setup:
    modules = 0

    def __init__(self, project_dict) -> None:
        self.obj = project_dict

    @staticmethod
    def main(auto=True, database=True):
        ins = Setup.generate_ins()

        ins.print_result("Setup processing...")
        data = ins.extract_data_from_file(
            auto, 
            ins.obj["input_file"]["path"], 
            ins.obj["input_file"]["basename"], 
            ins.obj["input_file"]["extension"],
            RSLTS_DIR
        )
        ins.update_project_modules(data)

        ins.print_result("DataReferencing processing...")
        reference = ins.reference_data_from_file(
            auto, 
            ins.obj["input_file"]["path"], 
            ins.obj["input_file"]["basename"], 
            ins.obj["input_file"]["extension"],
            data["content"]["body"]
        )
        ins.update_project_modules(reference)

        ins.print_result("DataComparing processing...")
        compared = ins.compare_data_from_file(
            auto, 
            ins.obj["input_file"]["path"], 
            ins.obj["input_file"]["basename"], 
            ins.obj["input_file"]["extension"],
            reference["content"]["referenced"]
        )
        ins.update_project_modules(compared)

        return ins

    @staticmethod
    def generate_ins():
        input_file = Setup.return_valid_file(
            input("Please enter the path to the file or directory: ").strip()
        )
        print("== Select a parent Client for the project ==")
        clients = db.Clients.fetch_and_print_data()
        client_id = Setup._display_directory_files(clients) + 1

        if client_id > 0:
            project_ins = Setup._verify_if_project_exists(str(client_id), "client_id", input_file)

            if project_ins:
                print("Succesfully instanciated project: ")
                print(project_ins.obj)
                return project_ins
        else:
            print(client_id)

    @staticmethod
    def _verify_if_project_exists(client_id:int, client_category:str, input_file:str):
        print("== Select a child Project ==")
        projects = db.Projects.read_all_from_category(client_id, client_category)
        project_id = Setup._display_directory_files(projects) + 1

        if project_id > 0:
            print("\nProject exists - Will move forward with a new version")
            project_ins = Setup._handle_exists(input_file, project_id)
        else:
            print("\nProject doesn't exist - Will move forward and create a new one")
            project_ins = Setup._handle_exists_not(client_id, input_file)

        return project_ins

    @staticmethod
    def _handle_exists(input_file:str, project_id:int):
        project = db.Projects.read(project_id)

        if project:
            return Setup.get_ins(input_file, **project)

    @staticmethod
    def get_ins(input_file, **project_metadata):
        project_ins_dict = {
            "input_file": dict(
                path = input_file.get("path"),
                basename = input_file.get("basename"),
                extension = input_file.get("extension"),
            ),
            "output_file": dict(
                parent_directory = "== SECRET ==",
                directories = {},
            ),
            "project": dict(
                metadata = {
                    "version": Setup._return_valid_entity_name(db.Versions, project_metadata.get("version_id")),
                    "client": Setup._return_valid_entity_name(db.Clients, project_metadata.get("client_id")),
                    "division": project_metadata.get("division"),
                    "label": Setup._return_valid_entity_name(db.Labels, project_metadata.get("label_id")),
                    "name": project_metadata.get("name"),
                    "code": project_metadata.get("code"),
                    "notes": project_metadata.get("notes"),
                    "workweek": project_metadata.get("workweek"),
                    "location": Setup._return_valid_entity_name(db.Locations, project_metadata.get("location_id")),
                    "assignee": Setup._return_valid_entity_name(db.Users, project_metadata.get("assignee_id")),
                    "status": Setup._return_valid_entity_name(db.Labels, project_metadata.get("status_id")),
                    "start_date": project_metadata.get("start"),
                    "finish_date": project_metadata.get("finish"),
                    "tags": Setup._return_valid_entity_name(db.Tags, project_metadata.get("tag_id")),
                },
                modules = {},
            ),
        }

        ins = Setup(project_ins_dict)

        return ins

    @staticmethod
    def _handle_exists_not(client_id:int, input_file:str):
        return Setup.create_ins(client_id, input_file)
            
    @staticmethod
    def create_ins(client_id:int, input_file:str):
        project_id = Setup._return_valid_project(client_id)

        project_ins_dict = {
            "input_file": dict(
                path = input_file.get("path"),
                basename = input_file.get("basename"),
                extension = input_file.get("extension"),
            ),
            "output_file": dict(
                parent_directory = "== SECRET ==",
                directories = {},
            ),
            "project": dict(
                metadata = db.Projects.read(project_id),
                modules = {},
            ),
        }

        ins = Setup(project_ins_dict)

        return ins

    @staticmethod
    def _return_valid_project(client_id:int):
        project_metadata = {
            "version": Setup._return_valid_entity_name(
                db.Versions, 
                2
            ),
            "client": Setup._return_valid_entity_name(
                db.Clients, 
                client_id
            ),
            "division": input("Enter project Division: ").strip(),
            "label": Setup._return_valid_entity_name(
                db.Labels, 
                Setup._return_valid_entity_id(db.Labels, table="labels")
            ),
            "name": input("Enter project Name: ").strip(),
            "code": input("Enter project Code: ").strip(),
            "notes": input("Enter project Notes: ").strip(),
            "workweek": input("Enter project Workweek (default: Mon-Sun): ").strip() or "Mon-Sun",
            "location": Setup._return_valid_entity_name(
                db.Locations, 
                Setup._return_valid_entity_id(db.Locations, table="locations")
            ),
            "assignee": Setup._return_valid_entity_name(
                db.Users,
                Setup._return_valid_entity_id(db.Users, table="users")
            ),
            "status": Setup._return_valid_entity_name(
                db.Labels, 
                8
            ),
            "start_date": input("Enter project Start Date: ").strip(),
            "finish_date": input("Enter project Finish Date: ").strip(),
            "tags": Setup._return_valid_entity_name(
                db.Tags, 
                Setup._return_valid_entity_id(db.Tags, table="tags")
            ),
        },

        print(project_metadata)
        """ project_id = db.Projects.create(project_metadata)

        return project_id """

    @staticmethod
    def _return_valid_entity_id(class_entity, table:str):
        option_list = class_entity.fetch_and_print_data()
        option_id = Setup._display_directory_files(option_list)

        if option_id > 0:
            return option_id
        else:
            response = Setup.binary_user_interaction(
                f"{table.capitalize()} does not exist. Would you like to create it? "
            )
            if response:
                essential_columns = class_entity.get_none_nullable_columns()
                inputs = {
                    item:input(f"Please give me the value for this field {item}").strip() 
                    for item in essential_columns
                }

                return class_entity.create(inputs)
            else:
                return None

    @staticmethod
    def _return_valid_entity_name(class_entity, entity_id:int):
        entity_details = class_entity.read(entity_id)

        return entity_details.get("name")

    @staticmethod
    def return_valid_file(input_file_dir:str) -> dict|int:
        if not os.path.exists(input_file_dir):
            raise FileNotFoundError("Error: Given directory or file does not exist in the system.")

        if os.path.isdir(input_file_dir):
            file_dict = Setup._handle_dir(input_file_dir)
        elif os.path.isfile(input_file_dir):
            file_dict = Setup._handle_file(input_file_dir)

        return file_dict

    @staticmethod
    def _handle_dir(input_file_dir:str, mode:str="r") -> dict|int:
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_file_dir)
            selection = Setup._display_directory_files(dir_list)
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
    def _handle_file(input_file_dir:str):
        input_file_extension = os.path.basename(input_file_dir).split(".")[-1]

        if (input_file_extension in ["xlsx", "xml"]):
            return dict(
                path = os.path.dirname(input_file_dir), 
                basename = os.path.basename(input_file_dir).split(".")[0],
                extension = input_file_extension,
            )

        print("Error: Please verify that the directory and file exist and that the file extension complies with class attributes")
        return -1

    @staticmethod
    def return_valid_date() -> str:
        now = datetime.now()
        date_str = now.strftime("%d-%b-%y %H:%M:%S")

        return date_str

    @staticmethod
    def return_valid_module_key() -> str:
        count = Setup.modules + 1
        Setup.modules = count

        return f"MODULE_{count}"

    @staticmethod
    def write_data_to_json(file_title:str, json_dict:dict):
        file = os.path.join(RSLTS_DIR, file_title)
        
        with open(file, 'w') as writer:
            json.dump(json_dict, writer)

    @staticmethod
    def ynq_user_interaction(prompt_message:str) -> str:
        valid_responses = {'y', 'n', 'q'}  
        
        while True:
            user_input = input(prompt_message).lower().strip()
            
            if user_input in valid_responses:
                return user_input  
            else:
                print("Error. Invalid input, please try again. ['Y/y' for Yes, 'N/n' for No, 'Q/q' for Quit]\n")\
                
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
    
    def extract_data_from_file(self, auto:str, input_file_path:str=None, input_file_basename:str=None, 
                                input_file_extension:str=None, output_file_dir:str=None) -> dict:
        data = XlsxDataIngestion.main(
            auto,
            input_file_path,
            input_file_basename,
            input_file_extension,
            output_file_dir
        )   

        return data

    def reference_data_from_file(self, auto:str, input_file_path:str=None, input_file_basename:str=None, 
                                  input_file_extension:str=None, project_data_dict:str=None) -> dict:
        reference = XlsxDataReferencing.main(
            auto,
            input_file_path,
            input_file_basename,
            input_file_extension,
            project_data_dict
        )

        return reference

    def compare_data_from_file(self, auto:str, input_file_path:str=None, input_file_basename:str=None, 
                                  input_file_extension:str=None, project_data_dict:str=None) -> dict:
        comparison = XlsxDataComparing.main(
            auto,
            input_file_path,
            input_file_basename,
            input_file_extension,
            project_data_dict
        )

        return comparison

    def update_project_modules(self, data:dict) -> None:
        module_key = self.return_valid_module_key()
        if module_key:
            self.obj["project"]["modules"][module_key] = data
        else:
            raise ValueError("Invalid module key")

    def print_result(self, prompt_message:str) -> None:
        print()
        print()
        print(f'//========== {prompt_message} ==========//')
        print()


if __name__ == "__main__":
    setup = Setup.main(False)
