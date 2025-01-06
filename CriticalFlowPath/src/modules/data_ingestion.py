import os
import re
import json
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime, date
from dateutil import parser
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, column_index_from_string

class DataIngestion:
    def __init__(self, input_file_path, input_file_basename, input_worksheet_name, input_json_path, 
                 input_file_id, input_project_code, input_project_title, input_project_subtitle, input_project_client, 
                 input_file_issue_date, input_file_created_at, input_file_updated_at, xlsx_start_row = 1, xlsx_start_col = 'A'):
        self.input_path = input_file_path
        self.input_basename = input_file_basename
        self.ws_name = input_worksheet_name
        self.output_json_path = input_json_path
        self.output_json_basename = DataIngestion.normalize_string(input_project_title)
        self.file_id = input_file_id
        self.project_code = input_project_code
        self.project_title = input_project_title
        self.project_subtitle = input_project_subtitle
        self.project_client = input_project_client
        self.file_issue_date = input_file_issue_date
        self.file_created_at = input_file_created_at
        self.file_updated_at = input_file_updated_at
        self.xlsx_start_row = xlsx_start_row
        self.xlsx_start_col = xlsx_start_col
        self.json_categories = ["phase", "location", "area", "trade", "activity_code"]
        self.allowed_headers = {
            "phase": ["phase"],
            "location": ["location"],
            "trade": ["trade"],
            "color": ["color"],
            "activity_code": ["activity_code", "code", "task_code", "act_code"],
            "activity_name": ["activity_name", "act_name"],
            "activity_status": ["activity_status", "status", "task_status"],
            "start": ["start", "start_date", "start_dates"],
            "finish": ["finish", "finish_date", "finish_dates", "end", "end_date"]
        }

        #Instance Results
        self.initial_project_type:str = None
        self.final_project_type:any = None
        self.final_project_dict:dict = None

    @staticmethod
    def main(auto=True, process_continuity=None, input_file=None, input_worksheet_name=None,
             input_json_file=None, input_json_title=None):
        if auto:
            project = DataIngestion.auto_generate_ins(process_continuity, input_file, input_worksheet_name,
                                                      input_json_file, input_json_title)
        else:
            project = DataIngestion.generate_ins()

        project_final = {}
        file_type = project.is_type_file(project.input_basename)

        if file_type == "xlsx":
            if project.ws_name is None:
                worksheet = input("Please enter the name for the new or existing worksheet: ")
            else:
                worksheet = project.ws_name

            reworked_json, nested_json = project.handle_xlsx(worksheet)
            project.write_json(reworked_json)
            project.write_json(nested_json, True)
            final_result = nested_json
        elif file_type == "xml":
            excel_dir = input("Please enter the directory to save the new Excel file: ")
            excel_path, excel_basename = DataIngestion.file_verification(excel_dir, 'e', 'c')
            reworked_json = project.handle_xml()
            final_result = project.create_wbs_table_to_fill(reworked_json, excel_path, excel_basename)
        
        project_final = {
            "init_file_type": file_type,
            "final_file_type": type(final_result),
            "final_project_dict": nested_json,
        }

        DataIngestion.document_project(project, project_final)
        return project

    @staticmethod
    def generate_ins():
        input_file = input("Please enter the path to the file or directory: ").strip()
        input_file_path = os.path.dirname(input_file)
        input_worksheet_name = None
        input_file_basename = os.path.basename(input_file)
        input_json_path = DataIngestion.return_valid_path()
        input_file_id = len([file for file in os.listdir(input_json_path) if file.endswith('json')])
        input_project_code = input("Enter Project CODE: ").strip()
        input_project_title = input("Enter Project Title: ").strip()
        input_project_subtitle = input("Enter Project Subtitle: ").strip()
        input_project_client = input("Enter Project Client: ").strip()
        input_file_issue_date = DataIngestion.return_valid_date()
        input_file_created_at = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
        input_file_updated_at = input_file_created_at

        ins =  DataIngestion(input_file_path, input_file_basename, input_worksheet_name, input_json_path, 
                             input_file_id, input_project_code, input_project_title, input_project_subtitle, 
                             input_project_client, input_file_issue_date, input_file_created_at, input_file_updated_at)
        
        return ins

    @staticmethod
    def auto_generate_ins(process_continuity, input_file, input_worksheet_name, 
                          input_json_file, input_json_title):
        
        if process_continuity == 'y':
            input_file_path, input_file_basename = DataIngestion.file_verification(
                input_file, 'excel', 'r')
            input_json_path, _ = DataIngestion.file_verification(
                    input_json_file, 'json', 'c')
            input_file_id = len([file for file in os.listdir(input_json_path) if file.endswith('json')])
            input_project_code = f"{input_json_title.strip()}_{input_file_id}"
            input_project_title = input_json_title.strip()
            input_project_subtitle = input_json_title.strip()
            input_project_client = input_json_title.strip()
            input_file_issue_date = DataIngestion.return_valid_date()
            input_file_created_at = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
            input_file_updated_at = input_file_created_at

            ins = DataIngestion(input_file_path, input_file_basename, input_worksheet_name, input_json_path, 
                                input_file_id, input_project_code, input_project_title, input_project_subtitle, 
                                input_project_client, input_file_issue_date, input_file_created_at, input_file_updated_at)
            
            return ins

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
    def file_verification(input_file_path, file_type, mode):
        if os.path.isdir(input_file_path):
            file_path, file_basename = DataIngestion.handle_dir(input_file_path, mode)
            if mode != 'c':
                path, basename = DataIngestion.handle_file(file_path, file_basename, file_type)
            else:
                path = file_path
                basename = file_basename
        elif os.path.isfile(input_file_path):
            file_path = os.path.dirname(input_file_path)
            file_basename = os.path.basename(input_file_path)
            path, basename = DataIngestion.handle_file(file_path, file_basename, file_type)

        return path, basename
    
    @staticmethod
    def handle_dir(input_path, mode):
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_path)
            selection = DataIngestion.display_directory_files(dir_list)
            base_name = dir_list[selection]
            print(f'File selected: {base_name}\n')
        elif mode == 'c':
            base_name = None
        else:
            print("Error: Invalid mode specified.")
            return -1
        
        return input_path, base_name

    @staticmethod
    def handle_file(file_path, file_basename, file_type):
        file = os.path.join(file_path, file_basename)

        valid_file_types = {
            "csv": "c",
            "excel": DataIngestion.is_xlsx(file),
            "json": DataIngestion.is_json(file),
            "pdf": "p",
        }

        if (valid_file_types[file_type]):
            return os.path.dirname(file), os.path.basename(file)
        
        print("Error: Please verify that the directory and file exist and that the file is of type .xlsx or .json")
        return -1

    @staticmethod
    def return_valid_path():
        while(True):   
            value = input("Please enter the directory to save the new JSON file: ").strip()
            try:
                if os.path.isdir(value):
                    return value
            except Exception as e:
                print(f"Error. {e}\n")

    @staticmethod
    def return_valid_date():
        while(True):   
            value = input("Enter Issue Date (format: dd-MMM-yyyy): ").strip()
            try:
                if datetime.strptime(value, "%d-%b-%Y"):
                    return value
            except Exception as e:
                print(f"Error. {e}\n")

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
    def normalize_string(entry_str:str) -> str:
        remove_bewteen_parenthesis = re.sub('(?<=\()(.*?)(?=\))', '', entry_str)
        special_chars = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        remove_special_chars = re.sub(special_chars, '', remove_bewteen_parenthesis.lower()).strip()
        normalized_str = re.sub(' ', '_', remove_special_chars)

        return normalized_str

    @staticmethod
    def document_project(project_ins, project_final:dict) -> None:
        project_ins.initial_project_type = project_final.get("init_file_type")
        project_ins.final_project_type = project_final.get("final_file_type")
        project_ins.final_project_dict = project_final.get("final_project_dict")

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
        reworked_json = self.fill_missing_dates(json_obj)
        earliest_start, latest_finish = self.project_dates(reworked_json)
        reworked_json["project_metadata"]["project_start"] = earliest_start
        reworked_json["project_metadata"]["project_finish"] = latest_finish

        # WIP
        #json_obj_with_locations = self.identify_location(reworked_json)

        nested_json = self.build_nested_dic(reworked_json)

        return reworked_json, nested_json
    
    def handle_xml(self):
        file = os.path.join(self.input_path, self.input_basename)

        tree = ET.parse(file)
        root = tree.getroot()
        ns = {'ms': 'http://schemas.microsoft.com/project'}

        xml_tasks = []
        for task in root.findall("./ms:Tasks/ms:Task", ns):
            xml_tasks.append(task)

        json_dict_list = []
        if xml_tasks:
            for task in xml_tasks:
                task_data = {child.tag.split('}')[-1]: child.text.strip() for child in task}
                json_dict_list.append(task_data)
        else:
            print("No <Task> elements found")

        return json_dict_list   

    def _xlsx_return_header(self, active_worksheet):
        ws = active_worksheet

        start_col = column_index_from_string(self.xlsx_start_col)
        header_list = []

        for row in ws.iter_rows(min_row=self.xlsx_start_row, max_row=self.xlsx_start_row, 
                                min_col=start_col, max_col= ws.max_column):
            for cell in row:
                if cell.value is not None:
                    normalized_str = self.normalize_string(cell.value)
                    header_tuple = (cell.coordinate, self._verify_header(normalized_str))
                    header_list.append(header_tuple)

        return header_list
    
    def _verify_header(self, entry_str:str) -> str:
        flat_allowed_headers = {value: key for key, values in self.allowed_headers.items() for value in values}

        if entry_str in flat_allowed_headers:
            result = flat_allowed_headers[entry_str]
        else:
            print(f"Warning. Header '{entry_str}' not found in declared dictionary")
            result = entry_str

        return result

    def json_fill_header(self, file_headers):
        json_obj_frame = {
            "project_metadata": {
                "project_id": self.file_id,
                "project_code": self.project_code,
                "project_title": self.project_title,
                "project_subtitle": self.project_subtitle,
                "project_client": self.project_client,
                "issue_date": self.file_issue_date,
                "project_start": None,
                "project_finish": None,
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

        first_header_col_letter, first_header_row = self.get_column_coordinates(
            header_dict, normalized_header[0][0]
        )
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
                    json_activity[key] = self.normalize_data_value(key, cell.value)
                else:
                    position = header_coordinates_list.index(parent_header)
                    key = header_key_list[position]
                    json_activity[key] = ""

            body_dict.append(json_activity)
            entry_counter += 1

        return json_obj

    def update_file(self):
        update_time = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
        self.update_file = update_time
        
        return self.update_file

    def fill_missing_dates(self, json_obj):
        body_dict = json_obj["project_content"]["body"]

        for item in body_dict:
            start = item.get("start")
            finish = item.get("finish")

            if start == "" and finish == "":
                print(f"Both 'start' and 'finish' are missing for entry: {item['entry']}")
            elif start == "":
                item["start"] = finish
            elif finish == "":
                item["finish"] = start
        
        json_obj["project_content"]["body"] = body_dict

        return json_obj

    def project_dates(self, json_obj):
        body_dict = json_obj["project_content"]["body"]
        
        start_list = [date["start"] for date in body_dict]
        finish_list = [date["finish"] for date in body_dict]

        earliest_start = self.bubble_sort_dates(start_list)[0]        
        latest_finish = self.bubble_sort_dates(finish_list)[-1]        

        return earliest_start, latest_finish

    def bubble_sort_dates(self, unsorted_list):
        n = len(unsorted_list)

        for i in range(n):
            for j in range(n-i-1):
                value_j = unsorted_list[j]
                value_j1 = unsorted_list[j+1]

                try:
                    if isinstance(value_j, str) and isinstance(value_j1, str):
                        value_j = datetime.strptime(value_j, "%d-%b-%Y").date()
                        value_j1 = datetime.strptime(value_j1, "%d-%b-%Y").date()

                    elif isinstance(value_j1, datetime):
                        value_j = value_j.date()
                        value_j1 = value_j1.date()

                except Exception as e:
                    print(f"Error: {e}")
                else:
                    if value_j > value_j1:
                        unsorted_list[j], unsorted_list[j+1] = unsorted_list[j+1], unsorted_list[j]
        
        return unsorted_list

    def get_column_coordinates(self, header_dict, header_key):
        coordinates = header_dict[header_key]

        row_match = re.search(r'\d+', coordinates)
        column_match = re.search(r'[a-zA-Z]+', coordinates)

        if not row_match or not column_match:
            raise ValueError(f"Invalid coordinates format: {coordinates}")

        row = int(row_match.group(0))
        column = column_match.group(0)

        return column, row 
        
    def normalize_data_value(self, header_column, cell_value):
        if isinstance(cell_value, str):
            if header_column == 'start' or header_column == 'finish':
                result = self.format_date_string(cell_value)
            else:
                result = cell_value.strip()

            return result
        elif isinstance(cell_value, date):
            return cell_value.strftime('%d-%b-%Y')
        elif isinstance(cell_value, int) or isinstance(cell_value, float):
            if cell_value == 0:
                cell_value = "0"
            return str(cell_value)
        else:
            return None

    def format_date_string(self, date_string, output_format="%d-%b-%Y"):
        try:
            special_chars = re.compile('[@_!#$%^&*()<>?\|}{~:]')

            if re.search(special_chars, date_string):
                cleaned_date_string = re.sub(special_chars, '', date_string)
            else:
                cleaned_date_string = re.sub("[a-zA-Z]$", '', date_string)
            

            parsed_date = parser.parse(cleaned_date_string.strip())
            formatted_date = parsed_date.strftime(output_format)

            return formatted_date
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None

    def write_json(self, json_obj, processed_json=False):
        if processed_json:
            file_name = f"processed_{self.output_json_basename}.json"
            file = os.path.join(self.output_json_path, file_name)
        else:
            file_name = f"{self.output_json_basename}.json"
            file = os.path.join(self.output_json_path, file_name)

        with open(file, 'w') as file_writer:
            json.dump(json_obj, file_writer)

        print(f"JSON data successfully created and saved to {file_name}.")

    def build_nested_dic(self, json_obj):
        metadata_dict = json_obj["project_metadata"]
        header_dict = json_obj["project_content"]["header"]
        body_dict = json_obj["project_content"]["body"]

        nested_dict = {
            "project_metadata": metadata_dict,
            "project_content": {
                "header": header_dict,
                "body": {}
            }
        }

        def dict_management(obj, key_list, recursive_dict):
            if not key_list:
                return recursive_dict

            current_key = key_list.pop(0)
            obj_key = obj.get(current_key)

            if obj_key is not None and obj_key != "":
                if len(key_list) < 1:
                    if obj_key not in recursive_dict:
                        recursive_dict[obj_key] = []
                    recursive_dict[obj_key].append(obj)
                else:
                    if obj_key not in recursive_dict:
                        recursive_dict[obj_key] = {}
                    dict_management(obj, key_list, recursive_dict[obj_key])
            else:
                if "M_DATA" not in recursive_dict:
                    recursive_dict["M_DATA"] = []
                recursive_dict["M_DATA"].append(obj)

            return recursive_dict


        for obj in body_dict:
            keys = [category for category in self.json_categories if obj.get(category) is not None]
            nested_dict["project_content"]["body"] = dict_management(
                obj, keys, nested_dict["project_content"]["body"]
            )
        
        return nested_dict

    def create_wbs_table_to_fill(self, data:list, excel_path, excel_basename):
        proc_table = self.generate_wbs_to_fill(data)
        self.write_data_to_excel(proc_table, excel_path, excel_basename)

        return proc_table

    def generate_wbs_to_fill(self, json_obj):
        df = pd.DataFrame(json_obj) 
        df.fillna("", inplace=True)

        return df

    def order_table_cols(self, column_list):
        for idx, col in enumerate(column_list):
            if col == "finish":
                temp = column_list[-1]
                column_list[-1] = col
                column_list[idx] = temp
                break
        
        return column_list

    def write_data_to_excel(self, proc_table, excel_path, excel_basename):
        if proc_table.empty:    
            print("Error. DataFrame is empty\n")
        else:
            excel_basename = self.input_basename.split('.')[0] + '.xlsx'
            file = os.path.join(excel_path, excel_basename)
            ws_name = "CFA - Fill Table"

            if not os.path.exists(excel_path):
                os.mkdir(excel_path)

            try:
                with pd.ExcelWriter(file, engine="openpyxl", mode='w') as writer:
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
    project = DataIngestion.main(False)

    #print(project.initial_project_type)
    #print(project.final_project_type)
    #print(project.final_project_dict)
