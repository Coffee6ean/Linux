import os
import json
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

class FilledExcelToUpdateJson():
    def __init__(self, input_excel_file_path):
        self.cpm_json_path = '/home/coffee_6ean/Linux/CriticalFlowPath/results/json/cpm.json'
        self.output_json_directory = '/home/coffee_6ean/Linux/CriticalFlowPath/results/json'
        self.default_ws_title = 'Project Content'
        self.excel_file_path = input_excel_file_path
        self.starting_data_row = 4
        self.final_data_col = 13
        self.json_categories = ['scope_of_work', 'phase', 'trade', 'company', 'location']
    
    @staticmethod
    def main():
        excel_input = input('Please enter the path to the Excel file or directory (or "q" to quit): ')
        if excel_input.lower() == 'q':
            print("Exiting the program.")
        else:
            try:
                selected_excel = FilledExcelToUpdateJson.file_verification(excel_input)
                filled_excel = FilledExcelToUpdateJson(selected_excel)

                # Update Existing JSON
                for category in filled_excel.json_categories:
                    filled_excel.update_json(filled_excel.extract_col_cells(category), category)

                # Create New JSON
                with open(filled_excel.cpm_json_path, 'r') as file:
                    json_obj = json.load(file)

                json_dic = {
                    "project_metadata": json_obj["project_metadata"],
                    "project_content": []
                }

                for category in filled_excel.json_categories:
                    test_json = filled_excel.extract_col_cells(category)      
                    json_dic["project_content"].append(filled_excel.create_json(test_json, category))

                filled_excel.write_json(json_dic)

                print("JSON file(s) updated successfully!")
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please check the file path and try again.")
        
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
    def file_verification(input_file_path):
        file_path = input_file_path

        if os.path.isdir(file_path):
            file_list = os.listdir(file_path)
            selection = FilledExcelToUpdateJson.display_directory_files(file_list)

            file_name = file_list[selection]

            print(f'File selected: {file_name}')
            file = os.path.join(file_path, file_name)
            if FilledExcelToUpdateJson.is_xlsx(file):
                return file
            else:
                return -1
        elif os.path.isfile(file_path):
            if FilledExcelToUpdateJson.is_xlsx(file_path):
                return file_path
            else:
                return -1
        else: 
            print('Error. Please verify the directory and file exist and that the file is of type .pdf')    
            return -1
    
    def worksheet_verification(self, workbook, worksheet_name=None):
        if worksheet_name is not None:
            worksheet_name = input('Please enter the name for the new or existing worksheet: ')
            if workbook[worksheet_name]:
                worksheet = workbook[worksheet_name]
            else:
                worksheet = workbook.create_sheet(worksheet_name)
        else:
            worksheet = workbook[self.default_ws_title]

        return worksheet

    def update_json(self, info_dic, dic_attr_type):
        with open(self.cpm_json_path, 'r') as json_file:
            data = json.load(json_file) 

        json_body = data["project_content"]["body"]

        phase_mapping = {entry["row"]: entry["value"] for entry in info_dic["body"]["filled"]}

        for activity in json_body:
            entry_row = activity.get('entry')
            if entry_row in phase_mapping:
                activity[dic_attr_type] = phase_mapping[entry_row]

            for sub_activity in activity.get('activities', []):
                sub_entry_row = sub_activity.get('entry')
                if sub_entry_row in phase_mapping:
                    sub_activity[dic_attr_type] = phase_mapping[sub_entry_row]

        with open(self.cpm_json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4) 

    def create_json(self, info_dic, category):
        flat_data = self.flattend_json_data()
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

    def write_json(self, json_dic):
        json_basename = 'reordered_cpm.json'

        with open(os.path.join(self.output_json_directory, json_basename), 'w') as json_file:
            json.dump(json_dic, json_file, indent=4)

        print(f"JSON data successfully created and saved to {json_basename}.")

    def flattend_json_data(self):
        flatten_list = []
        with open(self.cpm_json_path, 'r') as file:
            json_obj = json.load(file)

        for entry in json_obj['project_content']['body']:
            if 'activities' in entry:
                if len(entry['activities']) > 0:
                    flatten_list.extend(entry['activities'])
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

    def extract_col_cells(self, column_header):
        workbook = load_workbook(filename=self.excel_file_path)
        worksheet = self.worksheet_verification(workbook)

        json_dic = {
            "header": column_header,
            "body": {
                "filled": [],
                "empty": []
            }
        }

        phase_col_idx = self.find_column(worksheet, column_header)

        for row in worksheet.iter_rows(min_col=phase_col_idx, max_col=phase_col_idx, min_row=self.starting_data_row + 1, max_row=worksheet.max_row):
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

    def find_column(self, worksheet, column_header):
        for col in worksheet.iter_cols(min_row=self.starting_data_row, min_col=1, max_col=self.final_data_col):
            if any(isinstance(cell.value, str) and column_header in cell.value for cell in col if cell.value):
                return col[0].column
        return None

    def order_list(self, list):
        alphabtically_ordered_list = sorted(list)
        return alphabtically_ordered_list


if __name__ == '__main__':
    FilledExcelToUpdateJson.main()