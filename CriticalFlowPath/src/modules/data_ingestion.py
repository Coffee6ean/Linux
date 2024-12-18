import os
import re
import json
import pandas as pd
from typing import Union
from datetime import datetime, date
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

class DataIngestion:
    def __init__(self, input_file_path, input_file_basename, output_json_path, 
                 input_file_id, input_file_code, input_file_title, input_file_subtitle, input_file_issue_date, 
                 input_file_created_at, input_file_updated_at, xlsx_start_row = 1, xlsx_start_col = 'A'):
        self.input_path = input_file_path
        self.input_basename = input_file_basename
        self.output_json_path = output_json_path
        self.output_json_basename = DataIngestion.normalize_entry(input_file_title)
        self.file_id = input_file_id
        self.file_code = input_file_code
        self.file_title = input_file_title
        self.file_subtitle = input_file_subtitle
        self.file_issue_date = input_file_issue_date
        self.file_created_at = input_file_created_at
        self.file_updated_at = input_file_updated_at
        self.xlsx_start_row = xlsx_start_row
        self.xlsx_start_col = xlsx_start_col

    @staticmethod
    def main():
        project = DataIngestion.generate_ins()
        file_type = project.is_type_file(project.input_basename)

        if file_type == 'xlsx':
            worksheet = input("Please enter the name for the new or existing worksheet: ")
            project.handle_xlsx(worksheet)
            project.create_wbs_table_to_fill()

    @staticmethod
    def generate_ins():
        input_file = input("Please enter the path to the file or directory: ")
        input_file_path = os.path.dirname(input_file)
        input_file_basename = os.path.basename(input_file)
        output_json_path = input("Please enter the directory to save the new JSON file: ")
        input_file_id = len([file for file in os.listdir(output_json_path) if file.endswith('json')])
        input_file_code = input("Enter Document CODE: ")
        input_file_title = input("Enter Document Title: ")
        input_file_subtitle = input("Enter Document Subtitle: ")
        input_file_issue_date = input("Enter Issue Date (format: dd-MMM-yyyy)): ")
        input_file_created_at = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
        input_file_updated_at = input_file_created_at

        return DataIngestion(input_file_path, input_file_basename, output_json_path, 
                             input_file_id, input_file_code, input_file_title, input_file_subtitle, 
                             input_file_issue_date, input_file_created_at, input_file_updated_at)

    @staticmethod
    def is_type_file(input_basename):
        file_types = {
            "xlsx": ['e', 'excel', 'xlsx'],
            "csv": ['c', 'csv'],
            "json": ['j', 'json'],
            "xml": ['x', 'xml']
        }

        for file_type, extensions in file_types.items():
            if any(input_basename.endswith(ext) for ext in extensions):
                return file_type

        print("Unknown file type.")
        return None

    @staticmethod
    def display_directory_files(list):
        selection_idx = 0
        if len(list)==0:
            print("Error. No files found")
            return -1
        
        if len(list)>1:
            print(f"-- {len(list)} files found:")
            idx = 0
            for file in list:
                idx += 1
                print(f"{idx}. {file}")

            selection_idx = input("\nPlease enter the index number to select the one to process: ") 
        else:
            print(f"Single file found: {list[0]}")
            print("Will go ahead and process")

        return int(selection_idx) - 1

    @staticmethod
    def normalize_entry(entry_str):
        remove_bewteen_parenthesis = re.sub('(?<=\()(.*?)(?=\))', '', entry_str)
        special_chars = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        remove_special_chars = re.sub(special_chars, '', remove_bewteen_parenthesis.lower())
        normalized_str = re.sub(' ', '_', remove_special_chars)

        return normalized_str

    def update_file(self):
        update_time = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
        self.update_file = update_time
        
        return self.update_file

    def return_excel_workspace(self, worksheet_name):
        file = os.path.join(self.input_path, self.input_basename)
        
        try:
            workbook = load_workbook(filename=file)
            worksheet = workbook[worksheet_name]
        except KeyError:
            print(f"Error: Worksheet '{worksheet_name}' does not exist.")
            
            while True:
                user_answer = input("Would you like to create a new worksheet under this name? (Y/N/Q): ").strip().lower()
                
                if user_answer == 'y':
                    worksheet = workbook.create_sheet(worksheet_name)
                    self.ws_name = worksheet_name
                    print(f"New worksheet '{self.ws_name}' created.\n")
                    break
                elif user_answer == 'n':
                    ws_list = workbook.sheetnames
                    selected_ws_idx = DataIngestion.display_directory_files(ws_list)
                    
                    if selected_ws_idx >= 0:  
                        worksheet = workbook.worksheets[selected_ws_idx]
                        self.ws_name = ws_list[selected_ws_idx]
                        print(f"Worksheet selected: '{self.ws_name}'\n")
                        return workbook, worksheet
                    else:
                        print("Invalid selection. Returning without changes.\n")
                        return workbook, None
                        
                elif user_answer == 'q':
                    print("Quitting without changes.")
                    return workbook, None
                else:
                    print("Invalid input. Please enter 'Y' for Yes, 'N' for No, or 'Q' to Quit.")
        
        return workbook, worksheet

    def handle_xlsx(self, ws_name):
        wb, ws = self.return_excel_workspace(ws_name)
        file_headers = self._xlsx_return_header(ws)

        json_header = self.json_fill_header(file_headers)
        json_obj = self.json_fill_body(ws, json_header)
        json_obj["project_metadata"]["updated_at"] = self.update_file()

        self.write_json(json_obj)

    def _xlsx_return_header(self, active_worksheet):
        ws = active_worksheet

        start_col = column_index_from_string(self.xlsx_start_col)
        header_list = []

        for row in ws.iter_rows(min_row=self.xlsx_start_row, max_row=self.xlsx_start_row, 
                                min_col=start_col, max_col= ws.max_column):
            for cell in row:
                if cell.value is not None:
                    header_tuple = (cell.coordinate, self.normalize_entry(cell.value))
                    header_list.append(header_tuple)

        return header_list

    def json_fill_header(self, file_headers):
        json_obj_frame = {
            "project_metadata": {
                "file_id": self.file_id,
                "file_code": self.file_code,
                "file_title": self.file_title,
                "file_subtitle": self.file_subtitle,
                "issue_date": self.file_issue_date,
                "created_at": self.file_created_at,
                "updated_at": self.file_created_at
            },
            "project_content": {
                "header": {key: None for key in [
                    "entry", "phase", "location", "trade", "color",
                    "parent_id", "activity_code", "activity_id",
                    "activity_name", "activity_status", "activity_ins", 
                    "start", "finish", "total_float"
                ]},
                "body": []
            }
        }

        for coordinates, data in file_headers:
            header_dict = json_obj_frame["project_content"]["header"]

            header_dict[data] = coordinates

        return json_obj_frame

    def json_fill_body(self, active_worksheet, json_obj):
        ws = active_worksheet
        body_dict = json_obj["project_content"]["body"]
        header_dict = json_obj["project_content"]["header"]

        normalized_header = sorted(
            {k: v for k, v in header_dict.items() if v is not None}.items(), 
            key=lambda item: item[1]
        )

        header_coordinates_list = [dict_tuple[1] for dict_tuple in normalized_header]
        header_key_list = [dict_tuple[0] for dict_tuple in normalized_header]

        first_header_col_letter, first_header_row = self.get_column_coordinates(header_dict, normalized_header[0][0])
        last_header_col_letter, _ = self.get_column_coordinates(header_dict, normalized_header[-1][0])
        first_header_col = column_index_from_string(first_header_col_letter)
        last_header_col = column_index_from_string(last_header_col_letter)

        entry_counter = 1
        for row in ws.iter_rows(min_row=first_header_row + 1, max_row=ws.max_row, 
                                min_col=first_header_col, max_col=last_header_col):
            json_activity = {key: None for key in header_dict.keys()}
            json_activity["entry"] = entry_counter
            for cell in row:
                parent_header = next((val for val in header_coordinates_list if get_column_letter(cell.column) in val), None)
                if cell.value:        
                    position = header_coordinates_list.index(parent_header)
                    key = header_key_list[position]
                    json_activity[key] = self.check_date_data_type(cell.value)
                else:
                    position = header_coordinates_list.index(parent_header)
                    key = header_key_list[position]
                    json_activity[key] = ""

            body_dict.append(json_activity)
            entry_counter += 1

        return json_obj

    def get_column_coordinates(self, header_dict, header_key):
        coordinates = header_dict[header_key]

        row_match = re.search(r'\d+', coordinates)
        column_match = re.search(r'[a-zA-Z]+', coordinates)

        if not row_match or not column_match:
            raise ValueError(f"Invalid coordinates format: {coordinates}")

        row = int(row_match.group(0))
        column = column_match.group(0)

        return column, row 

    def check_date_data_type(self, date_val: Union[str, date]) -> str:
        if isinstance(date_val, str):
            return date_val
        elif isinstance(date_val, date):
            return date_val.strftime('%d-%b-%y %H:%M:%S')
        else:
            return -1

    def write_json(self, json_obj):
        file = os.path.join(self.output_json_path, f"{self.output_json_basename}.json")

        json_obj_with_locations = self.identify_location(json_obj)

        with open(file, 'w') as file_writer:
            json.dump(json_obj_with_locations, file_writer)

        print(f"JSON data successfully created and saved to {self.output_json_basename}.")

    def create_wbs_table_to_fill(self):
        proc_table = self.generate_wbs_to_fill()
        self.write_data_to_excel(proc_table)

    def generate_wbs_to_fill(self):
        json_file = os.path.join(self.output_json_path, f"{self.output_json_basename}.json")
        with open(json_file, 'r') as json_reader:
            json_obj = json.load(json_reader)

        df = pd.DataFrame(json_obj["project_content"]["body"])
        
        df[['phase', 'location', 'sub_location','trade', 'color']] = df[['phase', 'location', 'sub_location', 'trade', 'color']].fillna('')

        proc_table = pd.pivot_table(
            df,
            index=["activity_id", "activity_name"],
            values=["activity_code", "phase", "location", "sub_location", "trade", "color", "start", "finish"],
            aggfunc='first',
            fill_value=''
        )

        column_header_list = proc_table.columns.tolist()
        
        if "finish" in column_header_list and column_header_list[-1] != "finish":
            ordered_header_list = self.order_table_cols(column_header_list)
        else:
            ordered_header_list = column_header_list

        proc_table = proc_table[ordered_header_list]

        print(proc_table)

        return proc_table

    def order_table_cols(self, column_list):
        for idx, col in enumerate(column_list):
            if col == "finish":
                temp = column_list[-1]
                column_list[-1] = col
                column_list[idx] = temp
                break
        
        return column_list

    def write_data_to_excel(self, proc_table):
        if proc_table.empty:    
            print("Error. DataFrame is empty\n")
        else:
            file = os.path.join(self.input_path, self.input_basename)
            ws_name = "CFA - Fill Table"

            try:
                with pd.ExcelWriter(file, engine="openpyxl", mode='a', if_sheet_exists='replace') as writer:
                    proc_table.to_excel(
                        writer, 
                        sheet_name = ws_name, 
                        startrow = self.xlsx_start_row - 1, 
                        startcol = column_index_from_string(self.xlsx_start_col) - 1
                    )
                
                print(f"Successfully converted JSON to Excel and saved to: {file}")
                print(f"Saved to sheet: {ws_name}\n")
            except Exception as e:
                print(f"An unexpected error occurred: {e}\n")

    def identify_phase(self, json_obj):
        pass

    def identify_location(self, json_obj):
        body_dict = json_obj["project_content"]["body"]
        activity_names = [activity["activity_name"] for activity in body_dict]

        location_list = ["colo", "cell", "level", "zone", "area"]
        conventional_task_chars = re.compile("(?<=\W)[-_<>/|}{~:](?=\W)")
        prepositions_locations = re.compile("( for )|( in )|( at )|( on )|( inside )")

        for idx, name in enumerate(activity_names):
            normalized_name = name.lower().strip()
            has_special_chars_match = re.search(conventional_task_chars, normalized_name)
            has_prep_match = re.search(prepositions_locations, normalized_name)

            if has_special_chars_match:
                has_special_chars = has_special_chars_match.group(0)
                location_found = False
                components_found = normalized_name.split(has_special_chars)
                for component in components_found:
                    for location in location_list:
                        if location in component:
                            #print(component)
                            zone = component
                            self.check_for_subzone(zone, idx, body_dict)
                            location_found = True
                            break
                    
                    if location_found:
                        break
            elif has_prep_match:
                has_prep = has_prep_match.group(0)
                component = normalized_name.split(has_prep)[-1]
                for location in location_list:
                    if location in component:
                        zone = component
                        #print(component)
                        self.check_for_subzone(zone, idx, body_dict)
                        break
            else:
                body_dict[idx]["location"] = ""
    
        return json_obj

    def check_for_subzone(self, zone_name, element_idx, json_obj_body):
        location_keywords = ["colo", "cell", "level", "zone", "area"]
        conventional_subzone_chars = re.compile("[-<>/|}{~:\s]")
        normalized_name = zone_name.lower().strip()

        matched_locations = [location for location in location_keywords if location in normalized_name]

        if len(matched_locations) > 1:
            for location_type in matched_locations:
                match_style_one = re.search(f'{location_type}\s\d+', normalized_name)
                match_style_two = re.search(f'{location_type}\d+', normalized_name)

                if match_style_one:
                    formatted_match = re.sub(conventional_subzone_chars, '_', match_style_one.group(0)).upper()
                    if not json_obj_body[element_idx].get("location"):
                        json_obj_body[element_idx]["location"] = formatted_match
                    else:
                        json_obj_body[element_idx]["sub_location"] = formatted_match
                elif match_style_two:
                    formatted_match = re.sub(conventional_subzone_chars, '_', match_style_two.group(0)).upper()
                    if not json_obj_body[element_idx].get("location"):
                        json_obj_body[element_idx]["location"] = formatted_match
                    else:
                        json_obj_body[element_idx]["sub_location"] = formatted_match

        else:
            formatted_match = re.sub(conventional_subzone_chars, '', normalized_name).upper()
            json_obj_body[element_idx]["location"] = formatted_match
            json_obj_body[element_idx]["sub_location"] = ""


if __name__ == "__main__":
    DataIngestion.main()
    