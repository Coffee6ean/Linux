import os
import json
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

class FilledExcelToUpdateJson():
    def __init__(self, input_process_cont, input_excel_path, input_excel_basename, input_worksheet_name, 
                 input_json_path, input_json_basename):
        self.process_cont = input_process_cont
        self.file_path = input_excel_path
        self.file_basename = input_excel_basename
        self.ws_name = input_worksheet_name
        self.json_path = input_json_path
        self.json_basename = input_json_basename
        self.starting_data_row = 4
        self.final_data_col = 13
        self.json_categories = ["phase", "location", "trade", "activity_code"]
    
    @staticmethod
    def main():
        project = FilledExcelToUpdateJson.generate_ins()
        
        if project:
            try:
                wb, ws = project.return_excel_workspace(project.ws_name)

                if project.process_cont.lower() == 'y':
                    # Update Existing JSON
                    for category in project.json_categories:
                        project.update_json(project.extract_col_cells(ws, category), category)
                else:
                    # Generate New JSON
                    project.generate_new_json()
                    entry_frame = project.build_entry_dic(ws)
                    project.build_project_dic(ws, entry_frame)

                # Create Restructured JSON
                file = os.path.join(project.json_path, project.json_basename)
                with open(file, 'r') as f:
                    json_obj = json.load(f)

                json_dic = {
                    "project_metadata": json_obj["project_metadata"],
                    "project_content": []
                }

                json_dic["project_content"].append(project.build_nested_dic(entry_frame))
                project.write_json(json_dic)

                print("JSON file(s) updated successfully!")
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please check the file path and try again.")
        else:
            print("Exiting the program.")
        
    @staticmethod
    def generate_ins():
        input_excel_file = input("Please enter the path to the Excel file or directory (or 'q' to quit): ")
        if input_excel_file.lower() == 'q':
            print("Exiting the program.")
            return -1
        
        input_worksheet_name = input("Please enter the name for the new or existing worksheet: ")
        input_excel_path, input_excel_basename = FilledExcelToUpdateJson.file_verification(input_excel_file, 'e', 'f')

        input_process_cont = input("Is this part of the process or a new complete project? (Y/y for Yes, N/n for No): ")
        input_json_file = input("Please enter the directory to save the new JSON file: ")
        input_json_path, input_json_basename = FilledExcelToUpdateJson.file_verification(input_json_file, 'j', 's')

        ins = FilledExcelToUpdateJson(input_process_cont, input_excel_path, input_excel_basename, input_worksheet_name,
                                      input_json_path, input_json_basename)
        
        return ins

    @staticmethod
    def display_directory_files(list):
        selection_idx = 0
        if len(list)==0:
            print('Error. No files found')
            return -1
        
        if len(list)>1:
            print(f'{len(list)} files found:')
            idx = 0
            for file in list:
                idx += 1
                print(f'{idx}. {file}')

            selection_idx = input('\nPlease enter the index number to select the one to process: ') 
        else:
            print(f'Single file found: {list[0]}')
            print('Will go ahead and process')

        return int(selection_idx) - 1

    @staticmethod
    def is_json(file_name):
        if file_name.endswith('.json'):
            return True
        else:
            print('Error: Selected file is not a JSON file')
            return False

    @staticmethod
    def is_xlsx(file_name):
        if file_name.endswith('.xlsx'):
            return True
        else:
            print('Error. Selected file is not an Excel')
            return False

    @staticmethod
    def clear_directory(directory_path):
        if os.path.isdir(directory_path):
            file_list = os.listdir(directory_path)
            for file in file_list:
                file_path = os.path.join(directory_path, file)
                os.remove(file_path)

    @staticmethod
    def file_verification(input_file_path, file_type, mode):
        if os.path.isdir(input_file_path):
            path = input_file_path
            file = None

            if mode == 'f':
                dir_list = os.listdir(path)
                selection = FilledExcelToUpdateJson.display_directory_files(dir_list)
                base_name = dir_list[selection]
                print(f'File selected: {base_name}\n')
                file = os.path.join(path, base_name)
            elif mode == 's':
                base_name = None
                return path, base_name
            else:
                print("Error: Invalid mode specified.")
                return -1

            if (file_type == 'e' and FilledExcelToUpdateJson.is_xlsx(file)) or \
            (file_type == 'j' and FilledExcelToUpdateJson.is_json(file)):
                return path, base_name
            else:
                return -1
        elif os.path.isfile(input_file_path):
            if (file_type == 'e' and FilledExcelToUpdateJson.is_xlsx(input_file_path)) or \
            (file_type == 'j' and FilledExcelToUpdateJson.is_json(input_file_path)):
                path = os.path.dirname(input_file_path)
                base_name = os.path.basename(input_file_path)
                return path, base_name
            else:
                return -1
        else: 
            print('Error: Please verify that the directory and file exist and that the file is of type .xlsx or .json.')
            return -1
    
    def return_excel_workspace(self, worksheet_name):
        file = os.path.join(self.file_path, self.file_basename)
        
        try:
            workbook = load_workbook(filename=file)
            worksheet = workbook[worksheet_name]
        except KeyError:
            print(f"Error: Worksheet '{worksheet_name}' does not exist.")
            
            while True:
                user_answer = input("Would you like to create a new worksheet under this name? (Y/N/Q): ").strip().lower()
                
                if user_answer == 'y':
                    worksheet = workbook.create_sheet(worksheet_name)
                    print(f"New worksheet '{worksheet_name}' created.")
                    break
                elif user_answer == 'n':
                    ws_list = workbook.sheetnames
                    selected_ws = FilledExcelToUpdateJson.display_directory_files(ws_list)
                    worksheet = workbook.worksheets[selected_ws]
                    return workbook, worksheet
                elif user_answer == 'q':
                    print("Quitting without changes.")
                    return workbook, None
                else:
                    print("Invalid input. Please enter 'Y' for Yes, 'N' for No, or 'Q' to Quit.")
        
        return workbook, worksheet

    def update_json(self, info_dic, dic_attr_type):
        file = os.path.join(self.json_path, self.json_basename)

        with open(file, 'r') as json_file:
            data = json.load(json_file)

        json_body = data["project_content"]["body"]
        phase_mapping = {entry["row"]: entry["value"] for entry in info_dic["body"]["filled"]}

        for activity in json_body:
            activity[dic_attr_type] = None
            entry_row = activity.get('entry')

            if entry_row in phase_mapping:
                activity[dic_attr_type] = phase_mapping[entry_row]

            for sub_activity in activity.get('activities', []):
                sub_entry_row = sub_activity.get('entry')
                if sub_entry_row in phase_mapping:
                    sub_activity[dic_attr_type] = phase_mapping[sub_entry_row]

        with open(file, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def build_project_dic(self, active_ws, entry_frame):
        file = os.path.join(self.json_path, self.json_basename)
        ws = active_ws
        initial_col_idx = self.find_column(ws, self.json_categories[0])
        final_col_idx = self.find_column(ws, 'finish')
        entry_counter = 1
        json_dic = {
            "project_metadata": {},
            "project_content": {
                "header": list(entry_frame.keys()),
                "body": []
            }
        }
        header_list = list(entry_frame.keys())[1:]

        for row in ws.iter_rows(min_col=initial_col_idx, max_col=final_col_idx, 
                                min_row=self.starting_data_row + 1, max_row=ws.max_row):
            entry_frame["entry"] = entry_counter
            
            for header_counter, cell in enumerate(row):
                if header_counter < len(header_list): 
                    entry_frame[header_list[header_counter]] = cell.value

            if any(value is None or value == "" for value in entry_frame.values()):
                json_dic["project_content"]["body"].append(entry_frame.copy())
            else:
                json_dic["project_content"]["body"].append(entry_frame.copy()) 

            entry_counter += 1
        
        with open(file, 'w') as json_file:
            json.dump(json_dic, json_file, indent=4)

    def build_entry_dic(self, active_ws):
        ws = active_ws
        initial_col_idx = self.find_column(ws, self.json_categories[0])
        final_col_idx = self.find_column(ws, 'finish')

        for row in ws.iter_rows(min_col=initial_col_idx, max_col=final_col_idx, 
                                min_row=self.starting_data_row, max_row=self.starting_data_row):
            dic_frame = {
                "entry": None
            }

            if any(isinstance(cell.value, str) for cell in row if cell.value not in dic_frame):
                for cell in row:
                    if cell.value not in dic_frame and isinstance(cell.value, str):
                        new_key = cell.value.replace(" ", "_")
                        dic_frame[new_key.lower()] = None 

        return dic_frame

    def generate_new_json(self):
        json_basename = input("Please enter the name for the new JSON file: ") + ".json"
        self.json_basename = json_basename
        file = os.path.join(self.json_path, self.json_basename)
        
        try:
            with open(file, 'w') as json_file:
                json_pro = {
                    "project_metadata": {},
                    "project_content": {}
                } 

                json.dump(json_pro, json_file)
            print(f"New JSON file created: {file}")
            
        except Exception as e:
            print(f"An error occurred while creating the JSON file: {e}")

    def create_json(self, info_dic, category):
        file = os.path.join(self.json_path, self.json_basename)
        flat_data = self.flattend_json_data(file)
        ordered_type_list = self.flatten_col_typed_data(info_dic)

        json_dic = {
            "filled": {},
        }

        for activity in flat_data:
            entry = activity['entry']
            if entry in ordered_type_list['filled']:
                ordered_type_list['filled'][ordered_type_list['filled'].index(entry)] = activity
            elif entry in ordered_type_list['empty']:
                ordered_type_list['empty'][ordered_type_list['empty'].index(entry)] = activity
            else:
                print(f"Warning: Activity with entry {entry} not found in filled or empty lists.")

        for activity in ordered_type_list["filled"]:
            parent_key = activity.get(category)
            if parent_key not in json_dic["filled"]:
                json_dic["filled"][parent_key] = []  
            json_dic["filled"][parent_key].append(activity)

        ordered_type_list["filled"] = json_dic["filled"]
        
        return ordered_type_list

    def build_nested_dic(self, entry_frame):
        file = os.path.join(self.json_path, self.json_basename)
        flat_data = self.flattend_json_data(file)
        nested_dict = {}
        header_list = list(entry_frame.keys())

        for obj in flat_data:
            keys = [obj.get(category) for category in self.json_categories]
            key_one, key_two, key_three, key_four = keys

            if key_one is not None and key_one != None:
                if key_one not in nested_dict:
                    nested_dict[key_one] = {}
                
                if key_two is not None:
                    if key_two not in nested_dict[key_one]:
                        nested_dict[key_one][key_two] = {}
                    
                    if key_three is not None:
                        if key_three not in nested_dict[key_one][key_two]:
                            nested_dict[key_one][key_two][key_three] = {}
                        
                        if key_four is not None:
                            if key_four not in nested_dict[key_one][key_two][key_three]:
                                nested_dict[key_one][key_two][key_three][key_four] = []

                            entry_data = {header: obj.get(header) for header in header_list}
                            nested_dict[key_one][key_two][key_three][key_four].append(entry_data)

        return nested_dict
    
    def write_json(self, json_dic):
        json_basename = input("Please enter the name for the new or existing file: ") + ".json"
        file = open(os.path.join(self.json_path, json_basename), 'w')

        json.dump(json_dic, file, indent=4)
            
        print(f"JSON data successfully created and saved to {json_basename}.")

    def flattend_json_data(self, file_path):
        flatten_list = []
        with open(file_path, 'r') as file:
            json_obj = json.load(file)

        for entry in json_obj["project_content"]["body"]:
            if "activities" in entry:
                if len(entry["activities"]) > 0:
                    flatten_list.extend(entry["activities"])
                else:
                    flatten_list.append(entry)
            else:
                flatten_list.append(entry)
        
        return flatten_list

    def flatten_col_typed_data(self, info_dic):
        json_dic = {
            "header": info_dic["header"],
            "filled": [],
            "empty": []
        }

        for activity in info_dic["body"]["filled"]:
            json_dic["filled"].append(activity["row"])

        for activity in info_dic["body"]["empty"]:
            json_dic["empty"].append(activity["row"])

        return json_dic

    def extract_col_cells(self, active_ws, column_header):
        ws = active_ws
        json_dic = {
            "header": column_header,
            "body": {
                "filled": [],
                "empty": []
            }
        }
        phase_col_idx = self.find_column(ws, column_header)

        for row in ws.iter_rows(min_col=phase_col_idx, max_col=phase_col_idx, min_row=self.starting_data_row + 1, max_row=ws.max_row):
            for cell in row:
                cell_info = {
                    "value": cell.value,
                    "row": cell.row - self.starting_data_row
                }
                if cell.value is not None and isinstance(cell.value, str):
                    json_dic["body"]["filled"].append(cell_info)
                else:
                    json_dic["body"]["empty"].append(cell_info)

        return json_dic

    def find_column(self, active_ws, column_header):
        ws = active_ws

        for col in ws.iter_cols(min_row=self.starting_data_row, min_col=1, max_col=self.final_data_col):
            if any(isinstance(cell.value, str) and column_header in cell.value.lower() for cell in col if cell.value):
                return col[0].column
        return None

    def order_list(self, list):
        alphabtically_ordered_list = sorted(list)
        return alphabtically_ordered_list


if __name__ == '__main__':
    FilledExcelToUpdateJson.main()
