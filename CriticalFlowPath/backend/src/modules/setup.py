import os
import re
import json
from datetime import datetime

# Imported Helper - As Package 
from modules.utils.data_ingestion import DataIngestion
from modules.utils.data_frame_setup import DataFrameSetup
from modules.utils.data_relationship import DataRelationship
from modules.utils.data_processing import DataProcessing

# Imported Helper - As Module
""" from utils.data_ingestion import DataIngestion
from utils.data_frame_setup import DataFrameSetup
from utils.data_relationship import DataRelationship
from utils.data_processing import DataProcessing """

import sys
sys.path.append("../")
from backend.config.paths import RSLTS_DIR

class Setup:
    modules = 0

    def __init__(self, project_dict):
        self.obj = project_dict
    
    def __repr__(self):
        return (
            f"Setup("
            f"input_file={self.obj['input_file']}, "
            f"output_file={self.obj['output_file']}, "
            f"project={self.obj['project']})"
        )

    @staticmethod
    def main(payload:dict):
        ins = Setup.generate_ins(payload) 
 
        ins._print_result("DataIngestion processing...")
        data = ins._extract_data_from_file(
            payload["auto"], 
            ins.obj["input_file"]["path"], 
            ins.obj["input_file"]["basename"], 
            ins.obj["input_file"]["extension"],
            ins.obj["input_file"]["roi"],
            RSLTS_DIR
        )
        ins._update_project_modules(data)

        ins._print_result("DataFrameSetup processing...")
        frame = ins._frame_data_from_file(
            payload["auto"],
            ins.obj["input_file"]["path"], 
            ins.obj["input_file"]["basename"], 
            ins.obj["input_file"]["extension"],
            RSLTS_DIR,
            data["content"]
        )
        ins._update_project_modules(frame)

        """ ins._print_result("DataRelationship processing...")
        link = ins._link_data_from_file(
            payload["auto"],
            ins.obj["input_file"]["path"], 
            ins.obj["input_file"]["basename"], 
            ins.obj["input_file"]["extension"],
            RSLTS_DIR,
            data["content"],
        )
        ins._update_project_modules(link) """

        ins._print_result("DataProcessing processing...")
        proc = ins._process_data_from_file(
            payload["auto"],
            ins.obj["input_file"]["path"], 
            ins.obj["input_file"]["basename"], 
            ins.obj["input_file"]["extension"],
            data["details"]["start_date"],
            data["details"]["finish_date"],
            ins.obj["project"]["metadata"]["workweek"],
            RSLTS_DIR,
            frame["content"]["custom_ordered_dict"],
        )
        ins._update_project_modules(proc)
        ins.obj["status"] = "success"
        
        return ins
        
    @staticmethod
    def generate_ins(payload_dict:dict):
        if not payload_dict:
            input_file = Setup.return_valid_file(
                input("Please enter the path to the file or directory: ").strip()
            )
            input_file_roi = ""
            input_project_client = input("Enter Project Client: ").strip()
            input_project_name = input("Enter Project Name: ").strip()
            input_project_code = input("Enter Project Code: ").strip()
            input_project_title = input("Enter Project Title: ").strip()
            input_project_subtitle = input("Enter Project Subtitle: ").strip()
            input_project_workweek = input("Enter Project Workweek (default. Mon-Sun): ").strip()
            input_project_location = input("Enter Project Location: ").strip()
            input_project_asignee = input("Enter Project Assignee: ").strip()
            input_project_tags = input("Enter Project Tags: ").strip()
        else:
            input_file = Setup.return_valid_file(payload_dict["file_name"])
            input_file_roi = payload_dict["file_roi"]
            input_project_client = payload_dict["project_client"]
            input_project_name = payload_dict["project_name"]
            input_project_code = payload_dict["project_code"]
            input_project_title = payload_dict["project_title"]
            input_project_subtitle = payload_dict["project_subtitle"]
            input_project_workweek = payload_dict.get("project_workweek", "Mon-Sun")
            input_project_location = payload_dict["project_location"]
            input_project_asignee = payload_dict["project_assignee"]
            input_project_tags = payload_dict["project_tags"]

        project_ins_dict = {
            "input_file": dict(
                path=input_file.get("path"),
                basename=input_file.get("basename"),
                extension=input_file.get("extension"),
                roi=input_file_roi
            ),
            "output_file": dict(
                parent_directory="== SECRET ==",
                directories={},
            ),
            "project": dict(
                metadata=dict(
                    id=None,
                    continuity=None,
                    dates=dict(
                        created=Setup.return_valid_date(),
                        finished=None,
                    ),
                    client=input_project_client,
                    name=input_project_name,
                    code=input_project_code,
                    title=input_project_title,
                    subtitle=input_project_subtitle,
                    workweek=input_project_workweek,
                    location=input_project_location,
                    assignee=input_project_asignee,
                    tags=input_project_tags,
                ),
                modules={},
            ),
            "status": ""
        }

        return Setup(project_ins_dict)

    @staticmethod
    def return_valid_file(input_file_dir:str) -> dict|int:
        if not os.path.exists(input_file_dir):
            raise FileNotFoundError("Error: Given directory or file does not exist in the system.")

        if os.path.isdir(input_file_dir):
            file_dict = DataIngestion._handle_dir(input_file_dir)
        elif os.path.isfile(input_file_dir):
            file_dict = DataIngestion._handle_file(input_file_dir)

        return file_dict
    
    @staticmethod
    def _handle_dir(input_file_dir:str, mode:str="r") -> dict|int:
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_file_dir)
            selection = DataIngestion._display_directory_files(dir_list)
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
    def _handle_file(input_file_dir:str) -> dict:
        input_file_extension = os.path.basename(input_file_dir).split(".")[-1]

        if (input_file_extension in ["xlsx", "xml"]):
            return dict(
                path = os.path.dirname(input_file_dir), 
                basename = os.path.basename(input_file_dir).split(".")[0],
                extension = input_file_extension,
            )

        print("Error: Please verify that the directory and file exist and that the file extension complies with class attributes")
        return {}

    @staticmethod
    def normalize_string(entry_str:str) -> str:
        remove_bewteen_parenthesis = re.sub('(?<=\()(.*?)(?=\))', '', entry_str)
        special_chars = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        remove_special_chars = re.sub(special_chars, '', remove_bewteen_parenthesis.lower()).strip()
        normalized_str = re.sub(' ', '_', remove_special_chars)

        return normalized_str

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

    def _update_project_modules(self, data:dict) -> None:
        module_key = self.return_valid_module_key()
        if module_key:
            self.obj["project"]["modules"][module_key] = data
        else:
            raise ValueError("Invalid module key")

    def _extract_data_from_file(self, auto:str, input_file_path=None, input_file_basename=None, 
                                input_file_extension=None, input_file_roi=None, output_file_dir=None) -> dict:
        data = DataIngestion.main(
            auto,
            input_file_path,
            input_file_basename,
            input_file_extension,
            input_file_roi,
            output_file_dir
        )

        return data

    def _frame_data_from_file(self, auto:str, input_file_path=None, input_file_basename=None, 
                              input_file_extension=None, output_file_dir=None, project_data=None) -> dict:
        frame = DataFrameSetup.main(
            auto,
            input_file_path,
            input_file_basename,
            input_file_extension,
            output_file_dir,
            project_data
        )

        return frame

    def _link_data_from_file(self, auto:str, input_file_path=None, input_file_basename=None, 
                              input_file_extension=None, output_file_dir=None, project_data=None) -> dict:
        relationship = DataRelationship.main(
            auto,
            input_file_path,
            input_file_basename,
            input_file_extension,
            output_file_dir,
            project_data
        )

        return relationship

    def _process_data_from_file(self, auto:str, input_file_path=None, input_file_basename=None, 
                                input_file_extension=None, project_start_date=None, project_finish_date=None, 
                                input_file_workweek=None, output_file_dir=None, project_data=None) -> dict:
        processing = DataProcessing.main(
            auto,
            input_file_path,
            input_file_basename,
            input_file_extension,
            project_start_date,
            project_finish_date,
            input_file_workweek,
            output_file_dir,
            project_data
        )

        return processing

    def _print_result(self, prompt_message:str) -> None:
        print()
        print()
        print(f'//========== {prompt_message} ==========//')
        print()


if __name__ == "__main__":
    setup = Setup.main()
