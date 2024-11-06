import os
import json
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
            start_col = project.process_file(active_workbook, active_worksheet)
            project.style_file(active_workbook, active_worksheet, start_col)

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

    def process_file(self, active_workbook, active_worksheet):
        file = os.path.join(self.excel_path, self.excel_basename)
        wb = active_workbook

        print(f"Processing Excel file: {self.excel_basename}")
        start_col = self.find_column_idx(active_worksheet, "location") + 1
        end_col = self.find_column_idx(active_worksheet, "finish")

        """ self.validate_columns('scope_of_work')
        self.validate_columns('phase')
        self.validate_columns('trade')
        self.apply_post_processing() """

        self.delete_rows_per_location(active_worksheet)
        self.delete_columns(active_worksheet, start_col, end_col)

        wb.save(filename=file)
        return start_col

    def style_file(self, active_workbook, active_worksheet, start_col, start_row=1):
        file = os.path.join(self.excel_path, self.excel_basename)
        wb = active_workbook
        ws = active_worksheet

        year_list, year_row = self.same_cell_values(ws, start_col, start_row)
        for year in year_list:
            self.merge_same_value_cells(wb, ws, year, year_row)  

        month_list, month_row = self.same_cell_values(ws, start_col, start_row + 1)
        for month in month_list:
            self.merge_same_value_cells(wb, ws, month, month_row)  

        self.style_worksheet(ws, self.start_date, self.end_date, start_col, start_row)
        
        wb.save(filename=file)

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

    def apply_post_processing(self):
        file = os.path.join(self.file_path, self.file_basename)
        workbook = load_workbook(filename=file)
        ws = workbook[self.worksheet_name]

        first_row = ws[self.wbs_start_row ]
        
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

        workbook.save(file)
        print(f"Post-processing completed. Saved to {file}")
        workbook.close()

    def apply_post_sectioning(self, section_header):
        file = os.path.join(self.excel_path, self.excel_basename)
        workbook = load_workbook(filename=file)
        ws = workbook[self.ws_name]

        header_idx = self.find_column_idx(ws, section_header)
        finish_idx = self.find_column_idx(ws, 'finish')

        section_list = self.list_cell_values(ws, header_idx)
        last_valid_section = section_list[0]

        for row_idx, row in enumerate(ws.iter_rows(min_col=finish_idx + 1, max_col=ws.max_column, min_row=self.wbs_start_row + 1, max_row=ws.max_row)):
            current_section = section_list[row_idx]

            if current_section and current_section != last_valid_section:
                self.style_row_border(row)
                last_valid_section = current_section

        workbook.save(filename=file)
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

    def list_cell_values(self, active_ws, col_idx):
        ws = active_ws
        col_list = []

        if col_idx is not None:
            for row in ws.iter_rows(min_row=self.wbs_start_row + 1, min_col=col_idx, 
                                    max_col=col_idx, max_row=ws.max_row):
                for cell in row:
                    col_list.append(cell.value)
        
        return col_list 

    def find_column_idx(self, active_ws, column_header):
        ws = active_ws
        start_col_idx = column_index_from_string(self.wbs_start_col)
        normalized_header = column_header.replace(" ", "_").lower()

        for row in ws.iter_rows(min_row=self.wbs_start_row, min_col=start_col_idx, max_col=ws.max_column):
            for cell in row:
                if cell.value and isinstance(cell.value, str):
                    normalized_cell_value = cell.value.replace(" ", "_").lower()
                    if normalized_header in normalized_cell_value:
                        return cell.column

    def delete_columns(self, active_worksheet, start_column_idx, end_column_idx):
        ws = active_worksheet
        start_col_letter = get_column_letter(start_column_idx)
        end_col_letter = get_column_letter(end_column_idx)
        ws.delete_cols(start_column_idx, end_column_idx)
        
        print(f"Post column deletion applied successfully: [{start_col_letter}, {end_col_letter}]")

    def delete_rows_per_location(self, active_worksheet):
        ws = active_worksheet
        json_file = os.path.join(self.json_path, self.json_basename)

        with open(json_file, 'r') as json_reader:
            json_obj = json.load(json_reader)

        sorted_results, overlap_results = self.overlapping_dates(json_obj)

        overlap_processed = [result + 1 if result == 0 else result for result in overlap_results]

        existing_locations = []
        for i in range(len(overlap_processed)):
            existing_locations.append((list(set([activity["location"] for activity in sorted_results[i]]))[0], 
                                       overlap_processed[i]))

        self.delete_excess_rows(ws, "location", existing_locations)

        print("Excess rows removed successfully.")

    def delete_excess_rows(self, active_worksheet, column_header, existing_locations):
        ws = active_worksheet
        header_col = self.find_column_idx(active_worksheet, column_header)
        all_current_locations = [location[0] for location in existing_locations]

        rows_to_delete = []
        init_count = 0
        idx = 0
        for row in ws.iter_rows(min_row=self.wbs_start_row + 1,
                                        max_row=ws.max_row,
                                        min_col=header_col,
                                        max_col=header_col):
            for cell in row:
                if cell.value is not None:  
                    init_count = 0
                    if cell.value in all_current_locations:
                        idx = all_current_locations.index(cell.value)
                        rows = existing_locations[idx][1]

                if init_count > rows:
                    rows_to_delete.append(cell.row)
                
            init_count += 1

        for row in sorted(set(rows_to_delete), reverse=True):
            ws.delete_rows(row)

    def overlapping_dates(self, json_obj):
        body_dict = json_obj["project_content"][0]
        
        flatten_dict = self.flatten_json(body_dict)

        first_key = list(flatten_dict.keys())[0]
        location_ref = flatten_dict[first_key]["location"]
        location_based_lists = []
        nested_list = []

        for key, activity in flatten_dict.items():
            if flatten_dict[key]["location"] == location_ref:
                nested_list.append(activity)
            else:
                location_based_lists.append(nested_list)
                location_ref = activity["location"]
                nested_list = [activity]

        overlap_results = []
        sorted_results = []
        for location_list in location_based_lists:    
            sorted_list = self.bubble_sort_dates(location_list)
            start_ref = datetime.strptime(sorted_list[0]["start"], "%d-%b-%y")
            finish_ref = datetime.strptime(sorted_list[0]["finish"], "%d-%b-%y")

            overlap = 0
            result_overlap = 0
            for activity in sorted_list[1:]:
                start = datetime.strptime(activity["start"], "%d-%b-%y")
                finish = datetime.strptime(activity["finish"], "%d-%b-%y")

                if start >= start_ref or finish <= finish_ref:
                    overlap += 1

                if result_overlap < overlap:
                    result_overlap = overlap
                    overlap = 0

                start_ref = start
                finish_ref = finish

            overlap_results.append(result_overlap)
            sorted_results.append(sorted_list)

        return sorted_results, overlap_results

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

    def same_cell_values(self, active_ws, starting_col_idx, starting_row_idx):
        ws = active_ws

        iterable_row = ws[starting_row_idx]
        last_value = iterable_row[starting_col_idx].value  
        same_cell_list = []  
        overall_list = []  

        for cell in iterable_row[starting_col_idx:]:  
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

    def merge_same_value_cells(self, active_workbook, active_worksheet, column_indices, starting_row_idx):
        file = os.path.join(self.excel_path, self.excel_basename)
        wb = active_workbook
        ws = active_worksheet
        
        if not column_indices:
            print("No columns to merge.")
            return

        first_col = column_indices[0]
        last_col = column_indices[-1]

        ws.merge_cells(start_row=starting_row_idx, start_column=first_col, 
                              end_row=starting_row_idx, end_column=last_col)
        
        wb.save(filename=file)

    def style_worksheet(self, active_worksheet, start_date, end_date, start_col, start_row):
        ws = active_worksheet
    
        start_datetime_obj = datetime.strptime(start_date, '%d-%b-%Y')
        end_datetime_obj = datetime.strptime(end_date, '%d-%b-%Y')
        duration = (end_datetime_obj - start_datetime_obj).days + 1  
        thin_border = Border(left=Side(style='thin'))
    
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
                for row in range(start_row + 2, ws.max_row + 1):  
                    cell = ws.cell(row=row, column=col)
                    cell.border = thin_border
    
        print("Workbook styled and saved successfully.")


if __name__ == "__main__":
    ExcelPostProcessing.main(False)
