import os
import json
from datetime import datetime

# Imported Helper - As Module
""" import setup """

class XlsxDataComparing:
    allowed_extensions = ["json", "xlsx"]

    def __init__(self, input_file_path, input_file_basename, 
                 input_file_extension, project_data_dict):
        #Module Attribuates
        self.file_path = input_file_path
        self.file_basename = input_file_basename
        self.file_extension = input_file_extension
        self.data_dict = project_data_dict

        #Structures
        self.entry_categories = {
            "naming": {
                "count": 0,
                "activities": []
            },
            "new": {
                "count": 0,
                "activities": []
            },
            "logic": {
                "count": 0,
                "activities": []
            }, 
            "matching": {
                "count": 0,
                "activities": []
            },
            "updated": {
                "count": 0,
                "activities": []
            }, 
            "removed": {
                "count": 0,
                "activities": []
            }, 
        }
    
    @staticmethod
    def main(auto=True, input_file_path=None, input_file_basename=None, 
             input_file_extension=None, project_data_dict=None):
        if auto:
            project = XlsxDataComparing.auto_generate_ins(
                input_file_path, 
                input_file_basename, 
                input_file_extension, 
                project_data_dict
            )
        else:
            project = XlsxDataComparing.generate_ins()

        module_data = {
            "details": {
                "json": None,
                "activities": {
                    "count": 0,
                    "categorized": {}
                },
            },
            "logs": {
                "start": XlsxDataComparing.return_valid_date(),
                "finish": None,
                "run-time": None,
                "status": [],
            },
            "content": {
                "categorized": {},
                "compared": {}
            }
        }

        if project:
            comp_file = XlsxDataComparing.return_valid_file(input("Please enter the path to the file or directory: "))
            comp_dict = XlsxDataComparing.read_data_from_json(comp_file.get("path"), comp_file.get("basename"))
            comp_results = project.compare_data(project.data_dict, comp_dict["data"].get("content").get("compared"))
            module_data["details"]["activities"]["count"] = len(comp_results)
            module_data["details"]["activities"]["categorized"] = {key: value.get("count") for key, value in project.entry_categories.items()}
            module_data["content"]["categorized"] = {key: value.get("activities") for key, value in project.entry_categories.items()}
            module_data["content"]["compared"] = comp_results

        module_data["logs"]["finish"] = XlsxDataComparing.return_valid_date()
        module_data["logs"]["run-time"] = XlsxDataComparing.calculate_time_duration(
            module_data["logs"].get("start"), 
            module_data["logs"].get("finish")
        )

        return module_data

    @staticmethod
    def generate_ins():
        XlsxDataComparing.ynq_user_interaction(
            "Run Module as stand alone? "
        )

        setup_cls = setup.Setup.main()

        ins = XlsxDataComparing(
            setup_cls.obj["input_file"].get("path"), 
            setup_cls.obj["input_file"].get("basename"),
            setup_cls.obj["input_file"].get("extension"),
            setup_cls.obj["project"]["modules"]["MODULE_3"]["content"].get("compared"),
        )

        return ins

    @staticmethod
    def auto_generate_ins(input_file_path, input_file_basename, 
                          input_file_extension, project_data_dict):
        ins = XlsxDataComparing(
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
            file_dict = XlsxDataComparing._handle_dir(input_file_dir)
        elif os.path.isfile(input_file_dir):
            file_dict = XlsxDataComparing._handle_file(input_file_dir)

        return file_dict
    
    @staticmethod
    def _handle_dir(input_file_dir:str, mode:str="r") -> dict|int:
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_file_dir)
            selection = XlsxDataComparing._display_directory_files(dir_list)
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

        if (input_file_extension in XlsxDataComparing.allowed_extensions):
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

    def compare_data(self, new_dict:list, comp_dict:list, attribute:str="wbs_code") -> list:
        results = []

        comp_dict_lookup = {
            item[attribute]: item
            for item in comp_dict
            if item.get("activity_category").lower() not in {"invalid", "removed"}
        }

        for item in new_dict:
            if item.get("activity_category") == "invalid":
                continue
            
            if not item.get("activity_name"):
                continue

            target_value = item.get(attribute)

            match_comp_value = comp_dict_lookup.pop(target_value, {})

            updated_item = self._categorize_entries(item, match_comp_value)
            results.append(updated_item)

        for remaining_item in comp_dict_lookup.values():
            updated_item = self._build_result(remaining_item, {}, "removed")
            results.append(updated_item)

        print("Successfully compared data and labeled activity_category.")
        return results

    def _categorize_entries(self, entry:dict, comp:dict) -> dict:
        if not comp:
            category = "new"
            return self._build_result(entry, comp, category)

        if entry.get("wbs_code") == comp.get("wbs_code"):
            if entry.get("start") != comp.get("start") or entry.get("finish") != comp.get("finish"):
                category = "updated"
            elif entry.get("activity_name") != comp.get("activity_name"):
                category = "naming"
            else:
                category = "matching"
        else:
            category = "new"

        return self._build_result(entry, comp, category)

    def _build_result(self, entry:dict, comp:dict, category:str) -> dict:
        source = entry if not comp else comp

        result = {
            "entry": entry.get("entry"),
            "phase": source.get("phase"),
            "location": source.get("location"),
            "area": source.get("area"),
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
            "time_shift": self._calculate_time_shift(entry, comp), 
            "time_difference": self._calculate_time_difference(entry, comp),
            "total_float": entry.get("total_float"),
            "activity_predecessor_id": entry.get("activity_predecessor_id"),
        }

        self.entry_categories[category]["activities"].append(result)
        self.entry_categories[category]["count"] = self.entry_categories[category]["count"] + 1

        return result   

    def _calculate_time_difference(self, entry:dict, comp:dict) -> int:
        try:
            entry_start_obj = datetime.strptime(entry.get("start"), "%d-%b-%Y")
            entry_finish_obj = datetime.strptime(entry.get("finish"), "%d-%b-%Y")
            entry_duration = (entry_finish_obj - entry_start_obj).days + 1

            comp_start_obj = datetime.strptime(comp.get("start"), "%d-%b-%Y")
            comp_finish_obj = datetime.strptime(comp.get("finish"), "%d-%b-%Y")
            comp_duration = (comp_finish_obj - comp_start_obj).days + 1

            return entry_duration - comp_duration
        except (ValueError, TypeError):
            return 0

    def _calculate_time_shift(self, entry:dict, comp:dict) -> int:
        try:
            entry_start_obj = datetime.strptime(entry.get("start"), "%d-%b-%Y")
            comp_start_obj = datetime.strptime(comp.get("start"), "%d-%b-%Y")
            time_shift = (entry_start_obj - comp_start_obj).days + 1

            return time_shift
        except (ValueError, TypeError):
            return 0


if __name__ == "__main__":
    XlsxDataComparing.main(False)
