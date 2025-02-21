import os
import json
from datetime import datetime

# Imported Helper - As Module
""" import setup """

import sys
sys.path.append("../")
from CpmProcessor.keys.secrets import CLAYCO, TEST_JSON_DIR

class XlsxDataReferencing:
    allowed_extensions = ["json", "xlsx"]

    def __init__(self, input_file_path, input_file_basename, 
                 input_file_extension, project_data_dict):
        #Module Attribuates
        self.file_path = input_file_path
        self.file_basename = input_file_basename
        self.file_extension = input_file_extension
        self.data_dict = project_data_dict

        #Structures
        self.entry_statuses = {
            "new": [],
            "updated": [], 
            "modified": [],
            "matching": [], 
            "removed": [], 
            "duplicate": [], 
            "invalid": []
        }
    
    @staticmethod
    def main(auto=True, input_file_path=None, input_file_basename=None, 
             input_file_extension=None, project_data_dict=None):
        if auto:
            project = XlsxDataReferencing.auto_generate_ins(
                input_file_path, 
                input_file_basename, 
                input_file_extension, 
                project_data_dict
            )
        else:
            project = XlsxDataReferencing.generate_ins()

        module_data = {
            "details": {
                "json": None,
                "activities": {
                    "count": 0,
                    "categorized": {}
                },
            },
            "logs": {
                "start": XlsxDataReferencing.return_valid_date(),
                "finish": None,
                "run-time": None,
                "status": [],
            },
            "content": {
                "categorized": {},
                "referenced": {}
            }
        }

        if project:
            ref_dict = XlsxDataReferencing.read_data_from_json(CLAYCO, "reference_dictionary")
            cross_ref_results = project.cross_reference_new_data(ref_dict, project.data_dict)
            module_data["details"]["activities"]["count"] = len(cross_ref_results)
            module_data["details"]["activities"]["categorized"] = {key: len(value) for key, value in project.entry_statuses.items()}
            module_data["content"]["categorized"] = project.entry_statuses
            module_data["content"]["referenced"] = cross_ref_results

        module_data["logs"]["finish"] = XlsxDataReferencing.return_valid_date()
        module_data["logs"]["run-time"] = XlsxDataReferencing.calculate_time_duration(
            module_data["logs"].get("start"), 
            module_data["logs"].get("finish")
        )

        return module_data

    @staticmethod
    def generate_ins():
        XlsxDataReferencing.ynq_user_interaction(
            "Run Module as stand alone? "
        )

        setup_cls = setup.Setup.main()

        ins = XlsxDataReferencing(
            setup_cls.obj["input_file"].get("path"), 
            setup_cls.obj["input_file"].get("basename"),
            setup_cls.obj["input_file"].get("extension"),
            setup_cls.obj["project"]["modules"]["MODULE_1"].get("content"),
        )

        return ins

    @staticmethod
    def auto_generate_ins(input_file_path, input_file_basename, 
                          input_file_extension, project_data_dict):
        ins = XlsxDataReferencing(
            input_file_path, 
            input_file_basename, 
            input_file_extension,
            project_data_dict
        )

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
            file_dict = XlsxDataReferencing._handle_dir(input_file_dir)
        elif os.path.isfile(input_file_dir):
            file_dict = XlsxDataReferencing._handle_file(input_file_dir)

        return file_dict
    
    @staticmethod
    def _handle_dir(input_file_dir:str, mode:str="r") -> dict|int:
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_file_dir)
            selection = XlsxDataReferencing._display_directory_files(dir_list)
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
    def _handle_file(input_file_dir:str) -> dict|int:
        input_file_extension = os.path.basename(input_file_dir).split(".")[-1]

        if (input_file_extension in XlsxDataReferencing.allowed_extensions):
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
    def calculate_time_duration(start_date:str, finish_date:str, 
                                date_format:str="%d-%b-%y %H:%M:%S") -> float|int:
        try:
            start_time = datetime.strptime(start_date, date_format)
            finish_time = datetime.strptime(finish_date, date_format)

            minutes_duration = (finish_time - start_time).total_seconds()

            return minutes_duration
        except (ValueError, TypeError) as e:
            print(f"Error calculating runtime: {e}")
            return -1

    @staticmethod
    def read_data_from_json(file_path:str, file_basename:str, file_extension:str="json"):
        basename = f"{file_basename}.{file_extension}"
        file = os.path.join(file_path, basename)
        
        with open(file, 'r') as json_file:
            data = json.load(json_file)

        return data

    @staticmethod
    def write_dict_to_json(json_dict:dict, file_name:str, output_folder:str, mode:str='w') -> None:
        if not json_dict:
            print("Error: Dictionary is empty. No data to write.\n")
            return
        
        basename = file_name.split(".")[0] if "." in file_name else file_name
        new_directory = os.path.join(
            output_folder, 
            f"{basename}.json"
        )

        try:
            with open(new_directory, mode) as file_writer:
                json.dump(json_dict, file_writer)

            print(f"Successfully saved Dictionary to JSON:\nFile: {new_directory}\n")
        except Exception as e:
            print(f"An unexpected error occurred while writing to Excel: {e}\n")

    def cross_reference_new_data(self, ref_dict:dict, new_dict:list) -> list:
        results = []

        for item in new_dict:
            target_value = item.get("wbs_code")
            if not target_value:
                continue

            match_ref = self._search_for_existing_item(ref_dict, "wbs_code", target_value)
            updated_item = self._categorize_entries(item, match_ref.get("content") if match_ref else None)

            cross_ref_result = {
                "entry": updated_item.get("entry"),
                "bread_crumbs": match_ref.get("bread_crumbs") if match_ref else None,
                "phase": match_ref["content"].get("phase") if match_ref else None,
                "location": match_ref["content"].get("location") if match_ref else None,
                "area": match_ref["content"].get("area") if match_ref else None,
                "trade": match_ref["content"].get("trade") if match_ref else None,
                "color": match_ref["content"].get("color") if match_ref else None,
                "parent_id": match_ref["content"].get("entry") if match_ref else None,
                "activity_code": match_ref["content"].get("activity_code") if match_ref else None,
                "wbs_code": updated_item.get("wbs_code"),
                "activity_name": updated_item.get("activity_name"),
                "activity_status": updated_item.get("activity_status").upper() if updated_item.get("activity_status") else None,
                "activity_duration": updated_item.get("activity_duration"),
                "activity_ins": None,
                "start": updated_item.get("start"),
                "finish": updated_item.get("finish"),
                "total_float": None,
                "activity_predecessor_id": None,
                "activity_successor_id": None,
            }

            results.append(cross_ref_result)

        print("Successfully filled new model based on the existing reference")
        return results

    def _search_for_existing_item(self, ref_dict: dict, category: str, target_value: str, bread_crumbs: str = "") -> dict[str, any]:    
        if isinstance(ref_dict, dict):
            if category in ref_dict and ref_dict[category] == target_value:
                return {
                    "bread_crumbs": bread_crumbs.strip(" > "),
                    "content": ref_dict
                }

            for key, value in ref_dict.items():
                result = self._search_for_existing_item(value, category, target_value, bread_crumbs + f"{key} > ")
                if result:
                    return result

        elif isinstance(ref_dict, list):
            for idx, item in enumerate(ref_dict):
                result = self._search_for_existing_item(item, category, target_value, bread_crumbs + f"{idx} > ")
                if result:
                    return result  

        return None

    def _categorize_entries(self, entry:dict, reference:dict) -> dict:
        if reference is None:
            reference = {}

        if not entry.get("activity_name") and not entry.get("parent_id"):
            entry["activity_status"] = "invalid"
            self.entry_statuses["invalid"].append(entry)
            return entry

        if (entry.get("wbs_code") == reference.get("wbs_code") and 
            entry.get("activity_name") == reference.get("activity_name") and
            entry.get("start") == reference.get("start") and
            entry.get("finish") == reference.get("finish")):
            entry["activity_status"] = "matching"
            self.entry_statuses["matching"].append(entry)
            return entry

        #WIP - Improve labeling for data entries
        if (entry.get("wbs_code") == reference.get("wbs_code") and
            entry.get("activity_name") == reference.get("activity_name")):
            entry["activity_status"] = "updated"
            self.entry_statuses["updated"].append(entry)
            return entry

        if entry.get("wbs_code") == reference.get("wbs_code"):
            entry["activity_status"] = "modified"
            self.entry_statuses["modified"].append(entry)
            return entry

        if entry.get("activity_name") and not reference.get("activity_name"):
            entry["activity_status"] = "new"
            self.entry_statuses["new"].append(entry)
            return entry

        if reference.get("activity_name") and not entry.get("activity_name"):
            reference["activity_status"] = "removed"
            self.entry_statuses["removed"].append(reference)
            return reference

        if any(e for e in self.entry_statuses["duplicate"] 
            if e.get("activity_name") == entry.get("activity_name") and 
                e.get("wbs_code") == entry.get("wbs_code")):
            entry["activity_status"] = "duplicate"
            self.entry_statuses["duplicate"].append(entry)
            return entry

        return entry


if __name__ == "__main__":
    XlsxDataReferencing.main(False)
        