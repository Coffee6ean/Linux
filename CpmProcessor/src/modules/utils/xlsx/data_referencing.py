import os
import json
from datetime import datetime

# Imported Helper - As Module
""" import setup """

import sys
sys.path.append("../")
from CpmProcessor.keys.secrets import CLAYCO, MCGOUGH

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
        self.valid_sheet_name = {
            "table": ["table", "task"],
        }

        self.entry_categories = {
            "new": {
                "count": 0,
                "activities": []
            },
            "updated": {
                "count": 0,
                "activities": []
            }, 
            "modified": {
                "count": 0,
                "activities": []
            },
            "matching": {
                "count": 0,
                "activities": []
            }, 
            "removed": {
                "count": 0,
                "activities": []
            }, 
            "duplicate": {
                "count": 0,
                "activities": []
            }, 
            "invalid": {
                "count": 0,
                "activities": []
            }
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
            ref_dict = XlsxDataReferencing.read_data_from_json(CLAYCO, "ticket")
            cross_ref_results = project.cross_reference_new_data(
                ref_dict.get("data").get("body"), project.data_dict["content"]["body"]
            )
            module_data["details"]["activities"]["count"] = len(cross_ref_results)
            module_data["details"]["activities"]["categorized"] = {
                key: value.get("count") for key, value in project.entry_categories.items()
            }
            module_data["content"]["categorized"] = {
                key: value.get("activities") for key, value in project.entry_categories.items()
            }
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
            selection = XlsxDataReferencing._display_options(dir_list)
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
    def _display_options(file_list:list) -> list:
        if not file_list:
            print('Error: No elements found.')
            return []

        print(f'-- {len(file_list)} elements found:')
        for idx, file in enumerate(file_list, start=1):
            print(f'{idx}. {file}')

        result = []
        selection_input = input('\nEnter index numbers (comma-separated) to select elements to process: ').split(',')

        for selection in selection_input:
            selection = selection.strip()
            if not selection.isdigit():
                print(f'Error: Invalid input "{selection}", skipping.')
                continue

            index = int(selection)
            if 1 <= index <= len(file_list):
                result.append(index)
            else:
                print(f'Error: "{index}" is out of range (1 to {len(file_list)}).')

        return result

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

    def cross_reference_new_data(self, ref_dict:dict, new_dict:list, attribute:str="wbs_code") -> list:
        results = []

        for item in new_dict:
            target_value = item.get(attribute)

            if not target_value:
                continue

            match_ref = self._search_for_existing_item(ref_dict, attribute, target_value)
            updated_item = self._categorize_entries(item, match_ref if match_ref else {})

            results.append(updated_item)

        print("Successfully filled new model based on the existing reference")
        return results
    
    def _search_for_existing_item(self, ref_dict:dict, category:str, target_value:str) -> dict:    
        if isinstance(ref_dict, dict):
            if category in ref_dict and ref_dict[category] == target_value:
                return ref_dict

            for _, value in ref_dict.items():
                result = self._search_for_existing_item(value, category, target_value)
                if result:
                    return result

        elif isinstance(ref_dict, list):
            for item in ref_dict:
                result = self._search_for_existing_item(item, category, target_value)
                if result:
                    return result  

        return {}

    def _categorize_entries(self, entry:dict, reference:dict) -> dict:
        category = "new"

        if not entry.get("activity_name"):
            category = "invalid"
            return self._build_result(entry, reference, category)

        if (entry.get("wbs_code") == reference.get("wbs_code") and
            entry.get("start") == reference.get("start") and
            entry.get("finish") == reference.get("finish")):
            category = "matching"
            return self._build_result(entry, reference, category)

        if entry.get("wbs_code") == reference.get("wbs_code"):
            category = "modified"
            return self._build_result(entry, reference, category)

        if entry.get("wbs_code") and not reference.get("wbs_code"):
            category = "new"
            return self._build_result(entry, reference, category)

        if any(e for e in self.entry_categories["duplicate"]["activities"]
            if e.get("wbs_code") == entry.get("wbs_code")):
            category = "duplicate"
            return self._build_result(entry, reference, category)

        return self._build_result(entry, reference, category)

    def _build_result(self, entry:dict, reference:dict, category:str) -> dict:
        source = entry if not reference else reference

        result = {
            "entry": entry.get("entry"),
            "phase": source.get("phase"),
            "area": source.get("area"),
            "zone": source.get("zone"),
            "trade": source.get("trade"),
            "color": source.get("color"),
            "activity_code": source.get("activity_code"),
            "wbs_code": entry.get("wbs_code"),
            "activity_name": entry.get("activity_name"),
            "activity_category": category.upper(),
            "activity_status": entry.get("activity_status"),
            "activity_duration": entry.get("activity_duration"),
            "start": entry.get("start"),
            "finish": entry.get("finish"),
            "total_float": entry.get("total_float"),
            "successor_code": entry.get("successor_code"),
            "predecessor_code": entry.get("predecessor_code"),
        }

        self.entry_categories[category]["activities"].append(result)
        self.entry_categories[category]["count"] = self.entry_categories[category]["count"] + 1

        return result    


if __name__ == "__main__":
    XlsxDataReferencing.main(False)
        