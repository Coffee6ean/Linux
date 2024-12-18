import os
import json
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

class ExcelPostProcessing():
    def __init__(self, input_excel_path, input_excel_basename, input_worksheet_name, input_start_date,
                 input_end_date, input_json_path, input_json_basename, input_json_title):
        self.excel_path = input_excel_path
        self.excel_basename = input_excel_basename
        self.ws_name = input_worksheet_name
        self.start_date = input_start_date
        self.end_date = input_end_date
        self.json_path = input_json_path
        self.json_basename = input_json_basename
        self.json_title = input_json_title
        self.wbs_start_row = 4
        self.wbs_start_col = 'A'
        self.trade_list_validation = [
            'Bricklayer',
            'Carpenter',
            'Cement Mason',
            'Drywall Finisher',
            'Electrician',
            'Elevator Constructor',
            'Glazier',
            'Insulation Worker',
            'Ironworker',
            'Laborer',
            'Millwright',
            'N/A',
            'Operating Engineer',
            'Painter',
            'Pipefitter',
            'Roofer',
            'Sheet Metal Worker',
            'Plumber'
        ]
        self.phase_list_validation = [
            'Civil',
            'Comissioning',
            'Elevator',
            'Exteriors/Skin',
            'Foundations',
            'Framing Structure',
            'Garage',
            'Interior Finishes',
            'Interior Rough Ins',
            'Landscaping Decks',
            'N/A',
            'Roof',
            'Site Prep',
            'Site Utilities',
            'Structure',
            'Transformer Vault'
        ]
        self.scope_of_work_list_validation = [
            'Construction',
            'Concrete Works', 
            'Demolition',  
            'Electrical',
            'Finishes',
            'Framing',
            'HVAC',  
            'Insulation',  
            'Landscaping',  
            'N/A',
            'Painting',  
            'Paving',  
            'Plumbing',
            'Roofing',  
            'Site Work',
            'Structural Steel'
        ]
    
    @staticmethod
    def main(auto=True, input_excel_file=None, input_worksheet_name=None, input_start_date=None, 
             input_end_date=None, input_json_file=None, input_json_title=None):
        if auto:
            project = ExcelPostProcessing.auto_generate_ins(input_excel_file, input_worksheet_name, input_start_date,
                                                            input_end_date, input_json_file, input_json_title)
        else:
            project = ExcelPostProcessing.generate_ins()

        active_workbook, active_worksheet = project.return_excel_workspace(project.ws_name)
        
        if active_workbook and active_worksheet:
            json_dict, proc_table = project.setup_project()
            overlap_results = project.update_schedule_frame(active_workbook, active_worksheet, json_dict, proc_table)
            project.update_wbs_table(proc_table, overlap_results)

    @staticmethod
    def generate_ins():
        input_file_path = input("Please enter the path to the Excel file or directory: ")
        input_json_file = input("Please enter the path to the Json file or directory: ")
        input_start_date = input("Please enter the start date of the project (format: dd-MMM-yyyy): ")
        input_end_date = input("Please enter the end date of the project (format: dd-MMM-yyyy): ")

        input_excel_path, input_excel_basename = ExcelPostProcessing.file_verification(
            input_file_path, 'e', 'u')
        input_json_path, input_json_basename = ExcelPostProcessing.file_verification(
            input_json_file, 'j', 'r')
        
        if input_excel_path == -1:
            return None  

        input_worksheet_name = input("Please enter the name to create a worksheet: ")

        return ExcelPostProcessing(input_excel_path, input_excel_basename, input_worksheet_name, input_start_date,
                                   input_end_date, input_json_path, input_json_basename, None)

    @staticmethod
    def auto_generate_ins(input_excel_file, input_worksheet_name, input_start_date, 
                          input_end_date, input_json_file, input_json_title):
        input_excel_path, input_excel_basename = ExcelPostProcessing.file_verification(
            input_excel_file, 'e', 'u')
        
        input_json_path, input_json_basename = ExcelPostProcessing.file_verification(
            input_json_file, 'j', 'r')

        if input_excel_path == -1:
            return None  

        return ExcelPostProcessing(input_excel_path, input_excel_basename, input_worksheet_name, input_start_date, 
                                   input_end_date, input_json_path, input_json_basename, input_json_title)

    @staticmethod
    def file_verification(input_file_path, file_type, mode, input_json_title=None):
        if input_json_title and os.path.isdir(input_file_path):
            file_basename = f"processed_{input_json_title}.json"
            path, basename = ExcelPostProcessing.handle_file(input_file_path, file_basename, file_type)
        else:
            if os.path.isdir(input_file_path):
                file_path, file_basename = ExcelPostProcessing.handle_dir(input_file_path, mode)
                if mode != 'c':
                    path, basename = ExcelPostProcessing.handle_file(file_path, file_basename, file_type)
                else:
                    path = file_path
                    basename = file_basename
            elif os.path.isfile(input_file_path):
                file_path = os.path.dirname(input_file_path)
                file_basename = os.path.basename(input_file_path)
                path, basename = ExcelPostProcessing.handle_file(file_path, file_basename, file_type)

        return path, basename
    
    @staticmethod
    def handle_dir(input_path, mode):
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_path)
            selection = ExcelPostProcessing.display_directory_files(dir_list)
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

        if (file_type == 'e' and ExcelPostProcessing.is_xlsx(file)) or \
           (file_type == 'j' and ExcelPostProcessing.is_json(file)):
            return os.path.dirname(file), os.path.basename(file)
        
        print("Error: Please verify that the directory and file exist and that the file is of type .xlsx or .json")
        return -1

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
        if file_name.endswith(".json"):
            return True
        else:
            print("Error: Selected file is not a JSON file")
            return False

    @staticmethod
    def is_xlsx(file_name):
        if file_name.endswith('.xlsx'):
            return True
        else:
            print('Error. Selected file is not an Excel')
            return False

    def return_excel_workspace(self, worksheet_name):
        file = os.path.join(self.excel_path, self.excel_basename)
        
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
                    selected_ws_idx = ExcelPostProcessing.display_directory_files(ws_list)
                    
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

    def setup_project(self):
        flat_json_dict = self.read_json_dict()
        table, custom_order = self.design_json_table(flat_json_dict)
        proc_table = self.generate_wbs_cfa_style(table, custom_order, 'phase')

        return flat_json_dict, proc_table

    def update_schedule_frame(self, active_workbook, active_worksheet, json_dict, proc_table):
        file = os.path.join(self.excel_path, self.excel_basename)

        sorted_dict = self.bubble_sort_entries(json_dict)
        overlap_results = self.overlapping_dates(sorted_dict, proc_table)
        self.process_file(active_worksheet, overlap_results)

        active_workbook.save(filename=file)
        print("Schedule Frame successfully updated")
        active_workbook.close()

        return overlap_results

    def update_wbs_table(self, df_table, overlap_results):
        file = os.path.join(self.excel_path, self.excel_basename)

        wb = load_workbook(file)
        ws = wb[self.ws_name]
        phase_col_idx = self.find_column_idx(ws, "phase", self.wbs_start_row)
        location_col_idx = self.find_column_idx(ws, "location", self.wbs_start_row)
        start_col_idx = location_col_idx + 1
        end_col_idx = self.return_first_column_idx(ws, 1, 1)

        self.delete_columns(ws, start_col_idx, end_col_idx)
        self.merge_until_different_value(ws, phase_col_idx, self.wbs_start_row)
        self.merge_until_different_value(ws, location_col_idx, self.wbs_start_row)
        self.style_file(ws, start_col_idx)

        wb.save(filename=file)
        print("WBS Table successfully updated")
        wb.close()

    def process_file(self, active_worksheet, overlap_results):
        ws = active_worksheet

        print(f"Processing Excel file: {self.excel_basename}")
        
        wbs_start_col = column_index_from_string(self.wbs_start_col)
        start_col_idx = self.find_column_idx(ws, "location", self.wbs_start_row) + 1
        end_col_idx = self.return_first_column_idx(ws, 1, 1)

        self.unmerge_columns(ws, wbs_start_col, end_col_idx)
        self.delete_excess_rows(ws, "location", overlap_results)
        self.delete_columns(ws, start_col_idx, end_col_idx)
        self.insert_columns(ws, start_col_idx, end_col_idx - start_col_idx)
    
    def style_file(self, active_worksheet, start_col, start_row=1):
        ws = active_worksheet

        year_list, year_row = self.same_cell_values(ws, start_col, start_row)
        for year in year_list:
            self.merge_same_value_cells(ws, year, year_row)  

        month_list, month_row = self.same_cell_values(ws, start_col, start_row + 1)
        for month in month_list:
            self.merge_same_value_cells(ws, month, month_row)  

        self.style_worksheet(ws, self.start_date, self.end_date, start_col, start_row)
        self.apply_post_styling(ws)
        self.apply_post_sectioning(ws, "location", start_col)

    def validate_columns(self, header):
        file = os.path.join(self.excel_path, self.excel_basename)
        workbook = load_workbook(filename=file)
        ws = workbook[self.worksheet_name]

        first_row = ws[self.wbs_start_row ]  
        
        if first_row is None:
            print("Error: The first row is empty.")
            return

        if header == 'scope_of_work':
            validation_list = self.scope_of_work_list_validation
        elif header == 'phase':
            validation_list = self.phase_list_validation
        elif header == 'trade':
            validation_list = self.trade_list_validation
        else:
            print(f"Error: Invalid header '{header}'. Supported headers are 'scope_of_work', 'phase', and 'trade'.")
            return
        
        header_columns = [col for col in first_row if col.value and header.lower() in str(col.value).lower()]

        if not header_columns:
            print(f"No columns found matching header: '{header}'")
            return

        for col in header_columns:
            col_index = col.column  

            dv = DataValidation(
                type='list',
                formula1=f'"{",".join(validation_list)}"',
                allow_blank=True
            )
            dv.error = 'Your entry is not in the list'
            dv.errorTitle = 'Invalid Entry'
            dv.prompt = 'Please select from the list'
            dv.promptTitle = 'List Selection'
            
            ws.add_data_validation(dv)
            
            dv.add(f'{get_column_letter(col_index)}2:{get_column_letter(col_index)}{ws.max_row}')
        
        workbook.save(file)
        print(f"Data validation applied to columns matching '{header}' successfully.")
        workbook.close()

    def apply_post_styling(self, active_worksheet):
        ws = active_worksheet
        first_row = ws[self.wbs_start_row]
        
        if first_row is None:
            print("Error: The first row is empty.")
            return
        
        for cell in first_row:  
            cell.font = Font(name='Century Gothic', size=12, bold=True, color="FFFFFF")  
            cell.fill = PatternFill(start_color="00800080", end_color="00800080", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")  
        
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)  
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 1)  
            ws.column_dimensions[column_letter].width = adjusted_width

        for row in ws.rows:    
            if isinstance(row[0].value, int):
                parent_row = row
                for cell in parent_row:
                    cell.font = Font(name='Century Gothic', size=12, bold=True, color="00333333")  
                    cell.fill = PatternFill(start_color="00FFFFFF", end_color="00FFFFFF", fill_type="solid")
                    thin = Side(border_style="thin", color="000000")
                    cell.border = Border(bottom=thin)

        print(f"Post-styling successfully completed")

    def apply_post_sectioning(self, active_worksheet, section_header, start_col):
        ws = active_worksheet
        header_idx = self.find_column_idx(ws, section_header, self.wbs_start_row)

        section_list = self.list_cell_values(ws, header_idx)
        last_valid_section = section_list[0]

        for row_idx, row in enumerate(ws.iter_rows(min_col=start_col, 
                                                   max_col=ws.max_column, 
                                                   min_row=self.wbs_start_row + 1, 
                                                   max_row=ws.max_row)):
            current_section = section_list[row_idx]

            if current_section and current_section != last_valid_section:
                self.style_row_border(row)
                last_valid_section = current_section

        print("Post sectioning applied successfully.")

    def style_row_border(self, row):
        new_top_border = Side(border_style='dashed', color='000000')

        for cell in row:
            current_border = cell.border if cell.border else Border()
            new_border = Border(
                top=new_top_border, 
                left=current_border.left,  
                right=current_border.right,  
                bottom=current_border.bottom  
            )

            cell.border = new_border

    def list_cell_values(self, active_worksheet, col_idx):
        ws = active_worksheet
        col_list = []

        if col_idx is not None:
            for row in ws.iter_rows(min_row=self.wbs_start_row + 1, min_col=col_idx, 
                                    max_col=col_idx, max_row=ws.max_row):
                for cell in row:
                    col_list.append(cell.value)
        
        return col_list 

    def find_column_idx(self, active_ws, column_header, start_row):
        ws = active_ws
        start_col_idx = column_index_from_string(self.wbs_start_col)
        normalized_header = column_header.replace(" ", "_").lower()

        for row in ws.iter_rows(min_row=start_row, min_col=start_col_idx, max_col=ws.max_column):
            for cell in row:
                if cell.value and isinstance(cell.value, str):
                    normalized_cell_value = cell.value.replace(" ", "_").lower()
                    if normalized_header in normalized_cell_value:
                        return cell.column

    def return_first_column_idx(self, active_worksheet, start_row_idx, start_col_idx):
        ws = active_worksheet

        for row in ws.iter_rows(min_row=start_row_idx, min_col=start_col_idx, max_col=ws.max_column):
            for cell in row:
                if isinstance(cell.value, str) and cell.value:
                    return cell.column
        
        print(f"Error. No valid value encountered in specified row [{start_row_idx}, {start_row_idx}]")
        return -1

    def unmerge_columns(self, active_worksheet, start_column_idx, end_column_idx):
        ws = active_worksheet

        for merged_cell in list(ws.merged_cells.ranges):
            if (merged_cell.bounds[0] >= start_column_idx and 
                merged_cell.bounds[2] <= end_column_idx):
                ws.unmerge_cells(str(merged_cell))
        
        start_col_letter = get_column_letter(start_column_idx)
        end_col_letter = get_column_letter(end_column_idx)

        print(f"Column unmerging applied successfully: [{start_col_letter}, {end_col_letter}]")

    def delete_columns(self, active_worksheet, start_column_idx, end_column_idx):
        ws = active_worksheet

        amount_to_delete = end_column_idx - start_column_idx
        ws.delete_cols(start_column_idx, amount_to_delete)

        start_col_letter = get_column_letter(start_column_idx)
        end_col_letter = get_column_letter(end_column_idx)

        print(f"Columns deleted successfully: [{start_col_letter}, {end_col_letter}]")

    def insert_columns(self, active_worksheet, start_column_idx, num_cols):
        ws = active_worksheet

        for _ in range(num_cols):
            ws.insert_cols(start_column_idx)

        print(f"Columns ({num_cols}) added successfully")

    def write_data_to_excel(self, proc_table):
        if proc_table.empty:    
            print("Error. DataFrame is empty\n")
        else:
            file = os.path.join(self.excel_path, self.excel_basename)

            try:
                with pd.ExcelWriter(file, engine="openpyxl", mode='a', if_sheet_exists='overlay') as writer:
                    proc_table.to_excel(
                        writer, 
                        sheet_name=self.ws_name, 
                        startrow=self.wbs_start_row - 1, 
                        startcol=column_index_from_string(self.wbs_start_col) - 1
                    )
                
                print(f"Successfully converted JSON to Excel and saved to: {file}")
                print(f"Saved to sheet: {self.ws_name}\n")
            except Exception as e:
                print(f"An unexpected error occurred: {e}\n")

    def delete_excess_rows(self, active_worksheet, column_header, overlap_results):
        ws = active_worksheet
        header_col = self.find_column_idx(active_worksheet, column_header, self.wbs_start_row)
        all_current_locations = list(overlap_results.keys())

        rows_to_delete = []
        init_count = 0
        max_rows = 0
        for row in ws.iter_rows(min_row=self.wbs_start_row + 1,
                                        max_row=ws.max_row,
                                        min_col=header_col,
                                        max_col=header_col):
            for cell in row:
                if cell.value is not None:  
                    init_count = 0
                    if cell.value in all_current_locations:
                        if len(overlap_results[cell.value]) > 1:
                            max_rows = overlap_results[cell.value][0]
                            overlap_results[cell.value].pop(0)
                        else:
                            max_rows = overlap_results[cell.value][0]

                if init_count > max_rows:
                    rows_to_delete.append(cell.row)
                
            init_count += 1

        for row in sorted(set(rows_to_delete), reverse=True):
            ws.delete_rows(row)
        
        print("Excess rows removed successfully.")

    def read_json_dict(self):
        json_file = os.path.join(self.json_path, self.json_basename)

        with open(json_file, 'r') as json_reader:
            json_obj = json.load(json_reader)
        
        df = self.flatten_json(json_obj["project_content"][0])
        df_keys = list(df.keys())
        struct_dic = []

        for key in df_keys:
            phase_key = key.split('|')[0]
            location_key = key.split('|')[1]
            act_json_obj = {
                "phase": phase_key,
                "location": location_key,
                "trade": df[key].get("trade", None),
                "entry": df[key].get("entry", None),
                "activity_code": df[key].get("activity_code", ""),
                "activity_name": df[key].get("activity_name", ""),
                "activity_ins": key.split('|')[-1],
                "color": df[key].get("color", ""),
                "start": df[key].get("start", ""),
                "finish": df[key].get("finish", "")
            }

            struct_dic.append(act_json_obj)

        return struct_dic

    def design_json_table(self, flat_json_dict):
        custom_order = self.bring_category_to_top(flat_json_dict, "phase", "milestone")
        df_table = pd.DataFrame(flat_json_dict)

        return df_table, custom_order
    
    def bring_category_to_top(self, unordered_list, category, order_con):
        categorized_list = []
        normalized_category = category.lower().strip()
        normalized_value = order_con.lower().strip()

        sorted_list = sorted(set(item[normalized_category] for item in unordered_list if item.get(normalized_category) is not None))

        for item in sorted_list:
            if normalized_value in item.lower().strip():
                position = sorted_list.index(item)
                sorted_list.pop(position)
                categorized_list.append(item)

        custom_ordered_list = categorized_list + sorted_list
        
        return custom_ordered_list

    def overlapping_dates(self, json_dict, proc_table, alloted_space=2):
        custom_ordered_entry_list = proc_table['entry']
        custom_ordered_location_list = proc_table['location']

        location_based_lists = []
        nested_list = []
        ref_location = custom_ordered_location_list[0]

        for value in custom_ordered_entry_list:
            current_item = json_dict[value - 1]
            if current_item['location'] == ref_location:
                nested_list.append(current_item)
            else:
                location_based_lists.append(nested_list)
                nested_list = [current_item]
                ref_location = current_item['location']

        if nested_list:
            location_based_lists.append(nested_list)

        sorted_entries_list = []
        for location_list in location_based_lists:
            sorted_list = self.bubble_sort_dates(location_list)
            sorted_entries_list.append(sorted_list)

        overlap_results = self.calculate_overlap(sorted_entries_list, alloted_space)
        return overlap_results

    def calculate_overlap(self, location_based_lists, alloted_space=2):
        overlap_results = []

        for location_list in location_based_lists:
            active_overlaps = []
            max_overlap = 0
            location_ref = location_list[0]["location"]

            for activity in location_list:
                start = datetime.strptime(activity["start"], "%d-%b-%y")
                finish = datetime.strptime(activity["finish"], "%d-%b-%y")

                # Remove activities that have ended
                active_overlaps = [
                    (active_start, active_finish) 
                    for active_start, active_finish in active_overlaps 
                    if finish >= active_start and start <= active_finish
                ]

                # Add the current activity to active overlaps
                active_overlaps.append((start, finish))

                # Update the maximum overlap count
                max_overlap = max(max_overlap, len(active_overlaps))

            overlap_results.append((location_ref, max_overlap))

        max_rows_dict = {}
        for location, max_row in overlap_results:
            if location in max_rows_dict:
                max_rows_dict[location].append(max_row + alloted_space)
            else:
                max_rows_dict[location] = [max_row + alloted_space]

        return max_rows_dict

    def bubble_sort_entries(self, unsorted_list):
        n = len(unsorted_list)

        for i in range(n):
            for j in range(0, n-i-1):
                entry = unsorted_list[j]["entry"]
                entry_n1 = unsorted_list[j+1]["entry"]

                if entry > entry_n1:
                    unsorted_list[j], unsorted_list[j+1] = unsorted_list[j+1], unsorted_list[j]
        
        sorted_list = unsorted_list
        return sorted_list

    def flatten_json(self, json_obj):
        new_dic = {}

        def flatten(elem, flattened_key=""):
            if type(elem) is dict:
                keys_in_dic = list(elem.keys())

                if "entry" in keys_in_dic:
                    new_dic[flattened_key[:-1]] = elem
                else:
                    for current_key in elem:
                        flatten(elem[current_key], flattened_key + current_key + '|')
            elif type(elem) is list:
                i = 0
                for item in elem:
                    flatten(item, flattened_key + str(i) + '|')
                    i += 1
            else:
                new_dic[flattened_key[:-1]] = elem

        flatten(json_obj)

        return new_dic

    def bubble_sort_dates(self, unsorted_list):
        n = len(unsorted_list)

        for i in range(n):
            for j in range(0, n-i-1):
                date_typed_start = datetime.strptime(unsorted_list[j]["start"], "%d-%b-%y")
                date_typed_start_n1 = datetime.strptime(unsorted_list[j+1]["start"], "%d-%b-%y")

                if date_typed_start > date_typed_start_n1:
                    unsorted_list[j], unsorted_list[j+1] = unsorted_list[j+1], unsorted_list[j]

                elif date_typed_start == date_typed_start_n1:
                    date_typed_end = datetime.strptime(unsorted_list[j]["finish"], "%d-%b-%y")
                    date_typed_end_n1 = datetime.strptime(unsorted_list[j+1]["finish"], "%d-%b-%y")

                    if date_typed_end > date_typed_end_n1:
                        unsorted_list[j], unsorted_list[j+1] = unsorted_list[j+1], unsorted_list[j]
        
        sorted_list = unsorted_list
        return sorted_list
    
    def resize_dataframe(self, df, max_rows_dict):
        filtered_rows = []

        for location, max_rows_list in max_rows_dict.items():
            if len(max_rows_list) > 1:
                for max_rows in max_rows_list:
                    #print(f"  Phase max rows: {max_rows}")
                    location_rows = df[df['location'] == location]
                    limited_rows = location_rows.head(max_rows)
                    #print(f"  Limited rows for this phase:\n{limited_rows}")
                    filtered_rows.append(limited_rows)
            else:  # Single phase for the location
                max_rows = max_rows_list[0]
                #print(f"  Single max rows: {max_rows}")
                location_rows = df[df['location'] == location]
                limited_rows = location_rows.head(max_rows)
                #print(f"  Limited rows for this location:\n{limited_rows}")
                filtered_rows.append(limited_rows)

        result_df = pd.concat(filtered_rows)
        result_df.reset_index(drop=True, inplace=True)

        return result_df
  
    def generate_wbs_cfa_style(self, og_table, categories_list, category):
        og_table[category] = pd.Categorical(og_table[category], categories=categories_list, ordered=True)

        proc_table = pd.pivot_table(
            og_table,
            index=["phase", "location", "entry", "activity_code"],
            values=["color", "start", "finish"],
            aggfunc='first',
            observed=True
        )
        column_header_list = proc_table.columns.tolist()

        if "finish" in column_header_list and column_header_list[-1] != "finish":
            ordered_header_list = self.order_table_cols(column_header_list)
        else:
            ordered_header_list = column_header_list

        proc_table = proc_table[ordered_header_list]

        df_reset = proc_table.reset_index()

        return df_reset

    def order_table_cols(self, column_list):
        for idx, col in enumerate(column_list):
            if col == "finish":
                temp = column_list[-1]
                column_list[-1] = col
                column_list[idx] = temp
                break
        
        return column_list

    def same_cell_values(self, active_worksheet, starting_col_idx, starting_row_idx):
        ws = active_worksheet

        iterable_row = ws[starting_row_idx]
        last_value = iterable_row[starting_col_idx].value  
        same_cell_list = []  
        overall_list = []  

        for cell in iterable_row[starting_col_idx - 1:]:  
            if cell.value is None:
                break  
            elif cell.value == last_value:  
                same_cell_list.append(cell.column)  
            else:
                if same_cell_list:  
                    overall_list.append(same_cell_list)
                same_cell_list = [cell.column]  
                last_value = cell.value  

        if same_cell_list:
            overall_list.append(same_cell_list)

        return overall_list, starting_row_idx  

    def merge_same_value_cells(self, active_worksheet, column_indices, starting_row_idx):
        ws = active_worksheet
        
        if not column_indices:
            print("No columns to merge.")
            return

        first_col = column_indices[0]
        last_col = column_indices[-1]

        ws.merge_cells(start_row=starting_row_idx, start_column=first_col, 
                              end_row=starting_row_idx, end_column=last_col)

    def merge_until_different_value(self, active_worksheet, starting_col_idx, starting_row_idx):
        ws = active_worksheet

        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        current_merge_range = []
        merge_ranges = []

        for row_idx in range(starting_row_idx, ws.max_row + 1):
            cell = ws.cell(row=row_idx, column=starting_col_idx)

            if cell.value is not None:
                if current_merge_range:
                    merge_ranges.append(current_merge_range)
                current_merge_range = [cell]
            else:
                current_merge_range.append(cell)

        if current_merge_range:
            merge_ranges.append(current_merge_range)

        for merge_range in merge_ranges:
            if len(merge_range) > 1:
                start_row = merge_range[0].row
                end_row = merge_range[-1].row

                ws.merge_cells(
                    start_row=start_row,
                    start_column=starting_col_idx,
                    end_row=end_row,
                    end_column=starting_col_idx
                )

                for row in range(start_row, end_row + 1):
                    cell = ws.cell(row=row, column=starting_col_idx)
                    cell.border = thin_border

    def style_worksheet(self, active_worksheet, start_date, end_date, start_col, start_row):
        ws = active_worksheet
    
        start_datetime_obj = datetime.strptime(start_date, '%d-%b-%Y')
        end_datetime_obj = datetime.strptime(end_date, '%d-%b-%Y')
        duration = (end_datetime_obj - start_datetime_obj).days + 1  
    
        for cell in ws.iter_rows(min_row=start_row, max_row=start_row, 
                                        min_col=start_col, max_col=start_col + duration - 1):
            for cell in cell:  
                cell.font = Font(name='Century Gothic', size=12, bold=True, color="FFFFFF")  
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.fill = PatternFill(start_color='00800080', end_color='00800080', fill_type='solid')
    
        for cell in ws.iter_rows(min_row=start_row + 1, max_row=start_row + 1, 
                                        min_col=start_col, max_col=start_col + duration - 1):
            for cell in cell:  
                cell.font = Font(name='Century Gothic', size=12, bold=True, color="00333333")
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.fill = PatternFill(start_color='00CC99FF', end_color='00CC99FF', fill_type='solid')
    
        for cell in ws.iter_rows(min_row=start_row + 2, max_row=start_row + 2, 
                                        min_col=start_col, max_col=start_col + duration - 1):
            for cell in cell:  
                cell.font = Font(name='Century Gothic', size=12, bold=True, color="00000000")
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.fill = PatternFill(start_color='00C0C0C0', end_color='00C0C0C0', fill_type='solid')
        
        for row in ws.iter_rows(min_row=start_row + 3, min_col=start_col):  
            for cell in row:
                cell.alignment = Alignment(horizontal='center', vertical='center')
    
        for col in range(start_col, start_col + duration):
            last_month_cell = ws.cell(row=start_row + 1, column=col)  
            if last_month_cell.value is not None:  
                for row in range(start_row + 1, ws.max_row + 1):  
                    cell = ws.cell(row=row, column=col)

                    current_border = cell.border if cell.border else Border()
                    cell.border = Border(
                        top=current_border.top, 
                        left=Side(border_style="dashed"),  
                        right=current_border.right,  
                        bottom=current_border.bottom  
                    )
    
        print("Workbook styled and saved successfully.")


if __name__ == "__main__":
    ExcelPostProcessing.main(False)
