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
        self.entry_statuses = {
            "new": [],
            "logic": [],
            "matching": [],
            "updated": [], 
            "removed": []
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
            comp_ref_results = project.compare_data_2(comp_dict["data"].get("body"), project.data_dict)
            module_data["details"]["activities"]["count"] = len(comp_ref_results)
            module_data["details"]["activities"]["categorized"] = {key: len(value) for key, value in project.entry_statuses.items()}
            module_data["content"]["categorized"] = project.entry_statuses
            module_data["content"]["compared"] = comp_ref_results

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
            setup_cls.obj["project"]["modules"]["MODULE_1"].get("content"),
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

    def compare_data(self, comp_dict:dict, new_dict:list) -> list:
        results = []

        # Convert new_dict to a dictionary for faster lookups
        new_lookup = {item.get("wbs_code"): item for item in new_dict if item.get("wbs_code")}

        # Iterate through comp_dict to find matches in new_dict
        for item in comp_dict:
            target_value = item.get("wbs_code")
            if not target_value:
                continue

            # Find the matching entry in new_dict
            match = new_lookup.get(target_value)
            categorized_item = self._categorize_entries(item, match)

            # Skip invalid entries
            if categorized_item.get("activity_category") == "invalid":
                continue

            # Create the result entry
            comp_result = {
                "entry": match.get("entry") if match else None,
                "phase": match.get("phase") if match else None,
                "location": match.get("location") if match else None,
                "area": match.get("area") if match else None,
                "trade": match.get("trade") if match else None,
                "color": match.get("color") if match else None,
                "activity_code": match.get("activity_code") if match else None,
                "wbs_code": item.get("wbs_code"),
                "activity_name": match.get("activity_name") if match else None,
                "activity_category": categorized_item.get("activity_category").upper() if categorized_item.get("activity_category") else None,
                "activity_status": item.get("activity_status"),
                "activity_duration": match.get("activity_duration") if match else None,
                "activity_ins": item.get("activity_ins"),
                "start": match.get("start") if match else None,
                "finish": match.get("finish") if match else None,
                "difference": categorized_item.get("difference", 0),
                "total_float": match.get("total_float") if match else None,
                "activity_predecessor_id": match.get("activity_predecessor_id") if match else None,
            }

            results.append(comp_result)

        # Iterate through new_dict to find entries not in comp_dict (new entries)
        for item in new_dict:
            target_value = item.get("wbs_code")
            if not target_value:
                continue

            if target_value not in new_lookup:
                categorized_item = self._categorize_entries(item, None)

                # Skip invalid entries
                if categorized_item.get("activity_category") == "invalid":
                    continue

                # Create the result entry for new items
                comp_result = {
                    "entry": item.get("entry"),
                    "phase": item.get("phase"),
                    "location": item.get("location"),
                    "area": item.get("area"),
                    "trade": item.get("trade"),
                    "color": item.get("color"),
                    "parent_id": item.get("parent_id"),
                    "activity_code": categorized_item.get("activity_code"),
                    "wbs_code": item.get("wbs_code"),
                    "activity_name": categorized_item.get("activity_name"),
                    "activity_category": categorized_item.get("activity_category").upper() if categorized_item.get("activity_category") else None,
                    "activity_status": item.get("activity_status"),
                    "activity_duration": categorized_item.get("activity_duration"),
                    "activity_ins": item.get("activity_ins"),
                    "start": categorized_item.get("start"),
                    "finish": categorized_item.get("finish"),
                    "difference": categorized_item.get("difference", 0),
                    "total_float": item.get("total_float", ""),
                    "activity_predecessor_id": None,
                }

                results.append(comp_result)

        print("Successfully compared data and labeled activity_category.")
        return results

    def compare_data_2(self, comp_dict: dict, new_dict: list) -> list:
        results = []

        # Convert comp_dict to a dictionary for faster lookups
        comp_lookup = {item.get("wbs_code"): item for item in comp_dict if item.get("wbs_code")}

        # Iterate through new_dict to find matches in comp_dict
        for item in new_dict:
            target_value = item.get("wbs_code")
            if not target_value:
                continue

            # Find the matching entry in comp_dict
            match = comp_lookup.get(target_value)
            categorized_item = self._categorize_entries(item, match)

            # Skip invalid entries
            if categorized_item.get("activity_category") == "invalid":
                continue

            # Create the result entry
            comp_result = {
                "entry": item.get("entry"),
                "phase": item.get("phase"),
                "location": item.get("location"),
                "area": item.get("area"),
                "trade": item.get("trade"),
                "color": item.get("color"),
                "activity_code": item.get("activity_code"),
                "wbs_code": item.get("wbs_code"),
                "activity_name": item.get("activity_name"),
                "activity_category": categorized_item.get("activity_category").upper() if categorized_item.get("activity_category") else None,
                "activity_status": item.get("activity_status"),
                "activity_duration": item.get("activity_duration"),
                "activity_ins": item.get("activity_ins"),
                "start": item.get("start"),
                "finish": item.get("finish"),
                "difference": categorized_item.get("difference", 0),  # Default to 0 if not found
                "total_float": item.get("total_float", ""),  # Default to empty string if not found
                "activity_predecessor_id": item.get("activity_predecessor_id"),
            }

            results.append(comp_result)

        # Iterate through comp_dict to find entries not in new_dict (removed entries)
        for item in comp_dict:
            target_value = item.get("wbs_code")
            if not target_value:
                continue

            if target_value not in comp_lookup:
                categorized_item = self._categorize_entries(None, item)

                # Skip invalid entries
                if categorized_item.get("activity_category") == "invalid":
                    continue

                # Create the result entry for removed items
                comp_result = {
                    "entry": item.get("entry"),
                    "phase": item.get("phase"),
                    "location": item.get("location"),
                    "area": item.get("area"),
                    "trade": item.get("trade"),
                    "color": item.get("color"),
                    "activity_code": item.get("activity_code"),
                    "wbs_code": item.get("wbs_code"),
                    "activity_name": item.get("activity_name"),
                    "activity_category": categorized_item.get("activity_category").upper() if categorized_item.get("activity_category") else None,
                    "activity_status": item.get("activity_status"),
                    "activity_duration": item.get("activity_duration"),
                    "activity_ins": item.get("activity_ins"),
                    "start": item.get("start"),
                    "finish": item.get("finish"),
                    "difference": categorized_item.get("difference", 0),  # Default to 0 if not found
                    "total_float": item.get("total_float", ""),  # Default to empty string if not found
                    "activity_predecessor_id": item.get("activity_predecessor_id"),
                }

                results.append(comp_result)

        print("Successfully compared data and labeled activity_category.")
        return results

    def _search_for_existing_item(self, ref_dict:dict, category:str, target_value:str) -> dict[str, any]:    
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

        return None

    def _categorize_entries(self, entry:dict, comp:dict) -> dict:
        if comp is None:
            entry["activity_category"] = "new"
            self.entry_statuses["new"].append(entry)
            return entry

        if entry is None:
            comp["activity_category"] = "removed"
            self.entry_statuses["removed"].append(comp)
            return comp

        if entry.get("wbs_code") == comp.get("wbs_code"):
            if entry.get("start") != comp.get("start") or entry.get("finish") != comp.get("finish"):
                entry["activity_category"] = "updated"
                entry["difference"] = self._calculate_time_difference(entry, comp)
                self.entry_statuses["updated"].append(entry)
            else:
                entry["activity_category"] = "matching"
                self.entry_statuses["matching"].append(entry)
        else:
            entry["activity_category"] = "new"
            self.entry_statuses["new"].append(entry)

        return entry

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


if __name__ == "__main__":
    XlsxDataComparing.main(False)
        