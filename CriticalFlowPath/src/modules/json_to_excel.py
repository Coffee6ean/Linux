import os
import json
import pandas as pd
from openpyxl import Workbook

class JsonToExcel: 
    def __init__(self, input_file_path, input_file_basename, endpoint_file_path, 
                 endpoint_file_basename, xlsx_worksheet_name):
        self.json_file_path = input_file_path
        self.json_file_basename = input_file_basename
        self.xlsx_file_path = endpoint_file_path
        self.xlsx_file_basename = endpoint_file_basename
        self.worksheet_name = xlsx_worksheet_name

    @staticmethod
    def main():
        project = JsonToExcel.generate_ins()  
        project.write_data_to_excel()

    @staticmethod
    def generate_ins():
        input_file_path = input("Please enter the path to the JSON file or directory: ")
        input_path, input_base_name = JsonToExcel.file_verification(input_file_path)
        if input_path == -1:
            return None  

        endpoint_xlsx_path = input("Please enter the folder path to save the Excel file: ")
        endpoint_xlsx_basename = input("Please enter the name to save the file as: ") + ".xlsx"
        xlsx_worksheet_name = input("Please enter the name to create a worksheet: ")

        return JsonToExcel(input_path, input_base_name, endpoint_xlsx_path, endpoint_xlsx_basename, xlsx_worksheet_name)

    @staticmethod
    def file_verification(input_file_path):
        if os.path.isdir(input_file_path):
            path = input_file_path
            dir_list = os.listdir(path)
            selection = JsonToExcel.display_directory_files(dir_list)
            if selection == -1:
                return -1, None  

            base_name = dir_list[selection]
            print(f"File selected: {base_name}")
            file = os.path.join(path, base_name)

            if JsonToExcel.is_json(file):
                return path, base_name
            else:
                return -1, None
        elif os.path.isfile(input_file_path):
            if JsonToExcel.is_json(input_file_path):
                path = os.path.dirname(input_file_path)
                base_name = os.path.basename(input_file_path)
                return path, base_name
            else:
                return -1, None
        else: 
            print("Error: Please verify the directory and file exist and that the file is of type .json")    
            return -1, None

    @staticmethod
    def display_directory_files(list):
        if len(list) == 0:
            print("Error: No files found")
            return -1

        if len(list) > 1:
            print(f"-- {len(list)} files found:")
            for idx, file in enumerate(list, start=1):
                print(f"{idx}. {file}")
            selection_idx = input("\nPlease enter the index number to select the one to process: ")
        else:
            print(f"Single file found: {list[0]}")
            return 0  

        return int(selection_idx) - 1

    @staticmethod
    def is_json(file_name):
        if file_name.endswith(".json"):
            return True
        else:
            print("Error: Selected file is not a JSON file")
            return False

    def write_data_to_excel(self):
        excel_file = os.path.join(self.xlsx_file_path, self.xlsx_file_basename)
        json_file = os.path.join(self.json_file_path, self.json_file_basename)

        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return

        if data:
            with pd.ExcelWriter(excel_file, engine="openpyxl", mode='w') as writer:
                
                metadata = data.get("project_metadata", {})
                metadata_df = pd.DataFrame(metadata.items(), columns=["Field", "Value"])
                metadata_df.to_excel(writer, sheet_name="Metadata", index=False, startrow=1)
                body = data.get("project_content", {}).get("body", [])
                flattened_data = []

                for parent_data in body:
                    parent_obj_frame = {
                        "parent_id": "N/A",  
                        "id": parent_data.get("id", ""),
                        "name": parent_data.get("name", ""),
                        "duration": parent_data.get("duration", ""),
                        "start": parent_data.get("start", ""),
                        "finish": parent_data.get("finish", ""),
                        "total_float": parent_data.get("total_float", ""),
                        "scope_of_work": parent_data.get("scope_of_work", ""),
                        "phase": parent_data.get("phase", ""),
                        "trade": parent_data.get("trade", ""),
                        "company": parent_data.get("company", ""),
                        "location": parent_data.get("location", ""),
                    }
                    flattened_data.append(parent_obj_frame)

                    for child_data in parent_data.get("activities", []):
                        child_obj_frame = {
                            "parent_id": parent_data.get("id", ""),
                            "id": child_data.get("id", ""),
                            "name": child_data.get("name", ""),
                            "duration": child_data.get("duration", ""),
                            "start": child_data.get("start", ""),
                            "finish": child_data.get("finish", ""),
                            "total_float": child_data.get("total_float", ""),
                            "scope_of_work": child_data.get("scope_of_work", ""),
                            "phase": child_data.get("phase", ""),
                            "trade": child_data.get("trade", ""),
                            "company": child_data.get("company", ""),
                            "location": child_data.get("location", ""),
                        }
                        flattened_data.append(child_obj_frame)

                flattened_df = pd.DataFrame(flattened_data)
                flattened_df.to_excel(writer, sheet_name=self.worksheet_name, index=False, startrow=3)

            print(f"Successfully converted JSON to Excel and saved to {excel_file}")
        else:
            print("Error: No data to convert.")


if __name__ == "__main__":
    JsonToExcel.main()
