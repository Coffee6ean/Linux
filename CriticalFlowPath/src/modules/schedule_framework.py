import os
import json
from datetime import datetime, timedelta
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, column_index_from_string 
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

class ScheduleFramework():
    def __init__(self, input_file_path, input_file_name, input_worksheet_name, 
                 input_start_row, input_start_col, input_start_date, input_end_date):
        self.excel_path = input_file_path
        self.excel_basename = input_file_name
        self.ws_name = input_worksheet_name
        self.start_date = input_start_date
        self.end_date = input_end_date
        self.start_row = int(input_start_row)
        self.start_col = str(input_start_col)
        self.wbs_start_row = 4
        self.wbs_start_col = 'A'
        self.default_hex_font_color = "00FFFFFF"
        self.default_hex_fill_color = "00FFFF00"

    @staticmethod
    def main(auto=True, input_file_path=None, input_worksheet_name=None, 
             input_start_date=None, input_end_date=None):
        if auto:
            project = ScheduleFramework.auto_generate_ins(input_file_path, input_worksheet_name, 
                                                          input_start_date, input_end_date)
        else:
            project = ScheduleFramework.generate_ins()

        if project:
            active_workbook, active_worksheet = project.return_excel_workspace(project.ws_name)

            if active_workbook and active_worksheet:
                project.create_schedule_frame(active_workbook, active_worksheet)
            else:
                print("Error. Could not open Excel file as Workbook & Worksheet")

    @staticmethod
    def generate_ins():
        input_file_path = input("Please enter the path to the Excel file or directory: ")
        input_path, input_basename = ScheduleFramework.file_verification(input_file_path)
        input_worksheet_name = input("Please enter the name for the new or existing worksheet: ")
        input_start_row = input("Please enter the starting row to write the schedule: ")
        input_start_col = input("Please enter the starting column to write the schedule: ")
        input_start_date = input("Please enter the start date for the schedule (format: dd-MMM-yyyy): ")
        input_end_date = input("Please enter the end date for the schedule (format: dd-MMM-yyyy): ")
        ins = ScheduleFramework(input_path, input_basename, input_worksheet_name, input_start_row, 
                                input_start_col, input_start_date, input_end_date)

        return ins
    
    @staticmethod
    def auto_generate_ins(input_file_path, input_worksheet_name, input_start_date, input_end_date):
        input_start_row = 1
        input_start_col = ""

        input_path, input_basename = ScheduleFramework.file_verification(input_file_path, 'e', 'u')

        ins = ScheduleFramework(input_path, input_basename, input_worksheet_name, input_start_row, 
                                input_start_col, input_start_date, input_end_date)

        return ins

    @staticmethod
    def file_verification(input_file_path, file_type, mode):
        if os.path.isdir(input_file_path):
            file_path, file_basename = ScheduleFramework.handle_dir(input_file_path, mode)
            if mode != 'c':
                path, basename = ScheduleFramework.handle_file(file_path, file_basename, file_type)
            else:
                path = file_path
                basename = file_basename
        elif os.path.isfile(input_file_path):
            file_path = os.path.dirname(input_file_path)
            file_basename = os.path.basename(input_file_path)
            path, basename = ScheduleFramework.handle_file(file_path, file_basename, file_type)

        return path, basename
    
    @staticmethod
    def handle_dir(input_path, mode):
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_path)
            selection = ScheduleFramework.display_directory_files(dir_list)
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

        if (file_type == 'e' and ScheduleFramework.is_xlsx(file)) or \
           (file_type == 'j' and ScheduleFramework.is_json(file)):
            return os.path.dirname(file), os.path.basename(file)
        
        print("Error: Please verify that the directory and file exist and that the file is of type .xlsx or .json")
        return -1

    @staticmethod
    def display_directory_files(list):
        selection_idx = 0
        if len(list)==0:
            print('Error. No files found')
            return -1
        
        if len(list)>1:
            print(f'-- {len(list)} files found:')
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
                    print(f"New worksheet '{worksheet_name}' created.")
                    break
                elif user_answer == 'n':
                    ws_list = workbook.sheetnames
                    selected_ws = ScheduleFramework.display_directory_files(ws_list)
                    worksheet = workbook.worksheets[selected_ws]
                    return workbook, worksheet
                elif user_answer == 'q':
                    print("Quitting without changes.")
                    return workbook, None
                else:
                    print("Invalid input. Please enter 'Y' for Yes, 'N' for No, or 'Q' to Quit.")
        
        return workbook, worksheet

    def create_schedule_frame(self, active_workbook, active_worksheet):
        file = os.path.join(self.excel_path, self.excel_basename)

        if self.start_col == "" or self.start_col is None:
            self.start_col = get_column_letter(self.find_column_idx(active_worksheet, 'finish') + 1)

        results_dict = self.setup_file(active_worksheet)

        self.generate_schedule_frame(active_worksheet, self.start_date, self.end_date)  
        self.fill_schedule_cfa_style(active_workbook, active_worksheet, 
                                        results_dict["start_list"], results_dict["finish_list"], 
                                        results_dict["color_list"], results_dict["code_list"], 
                                        results_dict["location_list"])
        
        active_workbook.save(filename=file)
        print("CFA Schedule successfully created")
        active_workbook.close()

    def setup_file(self, active_worksheet):
        ws = active_worksheet

        start_date_col, finish_date_col = self.return_dates_idx(ws)
        start_dates_list, finish_dates_list = self.list_dates(ws, start_date_col, finish_date_col)

        phase_idx = self.find_column_idx(ws, 'phase')
        location_idx = self.find_column_idx(ws, 'location')
        trade_idx = self.find_column_idx(ws, 'trade')
        color_idx = self.find_column_idx(ws, 'color')
        code_idx = self.find_column_idx(ws, 'activity code')

        color_hex_list = self.extract_cell_attr(ws, color_idx)
        activity_code_list = self.extract_cell_attr(ws, code_idx)
        phase_list = self.extract_cell_attr(ws, phase_idx)
        location_list = self.extract_cell_attr(ws, location_idx)
        pro_hex_list = self.process_hex_val(color_hex_list)

        results_dict = {
            "phase_list": phase_list,
            "location_list": location_list,
            "code_list": activity_code_list,
            "color_list": pro_hex_list,
            "start_list": start_dates_list,
            "finish_list": finish_dates_list
        }

        return results_dict

    def generate_schedule_frame(self, active_worksheet, start_date, end_date):
        worksheet = active_worksheet

        start_datetime_obj = datetime.strptime(start_date, '%d-%b-%Y')
        end_datetime_obj = datetime.strptime(end_date, '%d-%b-%Y')
        duration = (end_datetime_obj - start_datetime_obj).days + 1  
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        for day in range(duration):
            date = start_datetime_obj + timedelta(days=day)
            worksheet.cell(row=self.start_row + 3, 
                           column=column_index_from_string(self.start_col) + day, 
                           value=weekdays[date.weekday()])
    
        for day in range(duration):
            date = start_datetime_obj + timedelta(days=day)
            worksheet.cell(row=self.start_row + 2, 
                           column=column_index_from_string(self.start_col) + day, 
                           value=date.strftime('%d'))

        for day in range(duration):
            date = start_datetime_obj + timedelta(days=day)
            worksheet.cell(row=self.start_row + 1, 
                           column=column_index_from_string(self.start_col) + day, 
                           value=date.strftime('%b'))
    
        for day in range(duration):
            date = start_datetime_obj + timedelta(days=day)
            worksheet.cell(row=self.start_row, 
                           column=column_index_from_string(self.start_col) + day, 
                           value=date.strftime('%Y'))

        print("Gantt chart generated successfully.")

    def return_dates_idx(self, active_ws):
        ws = active_ws
        start_col_idx = column_index_from_string(self.wbs_start_col)
        start_date_col = None
        end_date_col = None

        if ws.cell(row=self.wbs_start_row, column=column_index_from_string(self.wbs_start_col)).value is not None:
            for col in ws.iter_cols(min_row=self.wbs_start_row, max_row=self.wbs_start_row, 
                                    min_col=start_col_idx, max_col=ws.max_column):
                if any(isinstance(cell.value, str) and 'start' in cell.value.lower() for cell in col if cell.value):
                    start_date_col = col[0].column
                elif any(isinstance(cell.value, str) and 'finish' in cell.value.lower() for cell in col if cell.value):
                    end_date_col = col[0].column
                    break
        else:
            print("No columns found for 'start' and 'end'")
            return None, None

        #print("'Start Date' column: ", start_date_col)
        #print("'End Date' column: ", end_date_col)
        return start_date_col, end_date_col

    def list_dates(self, active_ws, start_date_col, end_date_col):
        ws = active_ws
        start_dates_list = []
        end_dates_list = []

        if start_date_col and end_date_col is not None:
            try:
                for row in ws.iter_rows(min_row=self.wbs_start_row + 1, min_col=start_date_col, 
                                        max_col=start_date_col, max_row=ws.max_row):
                    for cell in row:
                        if cell.value and isinstance(cell.value, (str, datetime)):
                            start_dates_list.append(cell.value)

                for row in ws.iter_rows(min_row=self.wbs_start_row + 1, min_col=end_date_col, 
                                        max_col=end_date_col, max_row=ws.max_row):
                    for cell in row:
                        if cell.value and isinstance(cell.value, (str, datetime)):
                            end_dates_list.append(cell.value)

            except Exception as e:
                print(f"An error occurred while extracting dates: {e}")
        else:
            return None, None

        #print("'Start Date' list: ", start_dates_list)
        #print("'End Date' list: ", end_dates_list)
        return start_dates_list, end_dates_list

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
    
    def process_hex_val(self, hex_dic_list):
        for hex_code in hex_dic_list:
            hex_code["value"] = hex_code["value"].replace('#', "00")
        
        return hex_dic_list

    def extract_cell_attr(self, active_ws, col_idx):
        ws = active_ws
        col_list = []

        if col_idx is not None:
            for row in ws.iter_rows(min_row=self.wbs_start_row + 1, min_col=col_idx, 
                                    max_col=col_idx, max_row=ws.max_row):
                for cell in row:
                    activity_cell = {
                        "alignment": {
                            "horizontal": cell.alignment.horizontal,
                            "vertical": cell.alignment.vertical,
                        },
                        "border": {
                            "top": cell.border.top,
                            "left": cell.border.left,
                            "right": cell.border.right,
                            "bottom": cell.border.bottom,
                        },
                        "fill": {
                            "start_color": cell.fill.start_color.rgb if cell.fill.start_color.rgb else cell.fill.start_color,
                            "end_color": cell.fill.end_color.rgb if cell.fill.start_color.rgb else cell.fill.start_color,
                            "fill_type": cell.fill.fill_type,
                        },
                        "font": {
                            "name": cell.font.name,
                            "size": cell.font.size,
                            "bold": cell.font.bold,
                            "color": cell.font.color,
                        },
                        "value": cell.value,
                    }

                    col_list.append(activity_cell)
        
        return col_list

    def fill_schedule_gantt_style(self, active_wb, active_ws, start_dates_list, 
                                  end_dates_list, color_hex_list, activity_code_list):
        wb = active_wb
        ws = active_ws
        file = os.path.join(self.excel_path, self.excel_basename)

        row_counter = 0
        for row in ws.iter_rows(min_row=self.start_row + 4, max_row=ws.max_row, 
                                min_col=column_index_from_string(self.start_col)):
            cell_counter = 0 
            for cell in row:
                cell_date = datetime.strptime(self.start_date, '%d-%b-%Y') + timedelta(days=cell_counter)
                start_date = datetime.strptime(start_dates_list[row_counter], '%d-%b-%y')
                end_date = datetime.strptime(end_dates_list[row_counter], '%d-%b-%y')

                if start_date <= cell_date <= end_date:
                    try:
                        cell.alignment = Alignment(horizontal=activity_code_list[row_counter]["alignment"]["horizontal"], 
                                               vertical=activity_code_list[row_counter]["alignment"]["vertical"])
                    except:
                        cell.alignment = Alignment(horizontal="center", vertical="center")
                    try:    
                        cell.border = Border(top=activity_code_list[row_counter]["border"]["top"], 
                                         left=activity_code_list[row_counter]["border"]["left"], 
                                         right=activity_code_list[row_counter]["border"]["right"], 
                                         bottom=activity_code_list[row_counter]["border"]["bottom"])
                    except:
                        cell.border = Border(top="thin", left="thin", right="thin", bottom="thin")
                        
                    try:
                        cell.fill = PatternFill(start_color=color_hex_list[row_counter]["value"], 
                                                end_color=color_hex_list[row_counter]["value"], 
                                                fill_type=color_hex_list[row_counter]["fill"]["fill_type"])
                    except:
                        color = color_hex_list[row_counter]["value"]
                        print(f"Color hex not found: {color}")
                        cell.fill = PatternFill(start_color=self.default_hex_fill_color, 
                                                end_color=self.default_hex_fill_color, 
                                                fill_type='solid')
                    try:
                        cell.font = Font(name=activity_code_list[row_counter]["font"]["name"], 
                                     size=activity_code_list[row_counter]["font"]["size"], 
                                     bold=activity_code_list[row_counter]["font"]["bold"], 
                                     color=activity_code_list[row_counter]["font"]["color"])
                    except:
                        cell.font = Font(name="Calibri", size="12", bold=True, color=self.default_hex_font_color)

                    cell.value = activity_code_list[row_counter]["value"]

                cell_counter += 1
            row_counter += 1

        wb.save(filename=file)
        print("Workbook filled successfully.")
        wb.close()

    def fill_schedule_cfa_style(self, active_workbook, active_worksheet, 
                                start_dates_list, end_date_list, 
                                color_hex_list, activity_code_list,
                                location_list):
        wb = active_workbook
        ws = active_worksheet
        
        start_ovr_date = datetime.strptime(self.start_date, '%d-%b-%Y')
        final_ovr_date = datetime.strptime(self.end_date, '%d-%b-%Y')
        last_valid_location = None  
        starting_point = self.wbs_start_row

        for idx, item in enumerate(start_dates_list):
            initial_date = datetime.strptime(item, '%d-%b-%y')
            final_date = datetime.strptime(end_date_list[idx], '%d-%b-%y')

            if initial_date >= start_ovr_date and final_date <= final_ovr_date:
                start_search_col = (initial_date - start_ovr_date).days
                finish_search_col = (final_date - start_ovr_date).days

                current_location = location_list[idx]["value"]
                if current_location is not None and current_location.strip() != "":
                    if current_location != last_valid_location:
                        starting_point = self.wbs_start_row + idx + 1
                        last_valid_location = current_location
                else:
                    starting_point = starting_point

                for row in ws.iter_rows(min_row=starting_point, 
                                        max_row=ws.max_row,
                                        min_col=column_index_from_string(self.start_col)+start_search_col, 
                                        max_col= column_index_from_string(self.start_col)+finish_search_col):
                    paint_row = True
                    
                    for cell in row:
                        if cell.value is not None:
                            paint_row = False
                            break
                    
                    if paint_row:
                        for cell in row:
                            try:
                                cell.alignment = Alignment(horizontal=activity_code_list[idx]["alignment"]["horizontal"], 
                                                vertical=activity_code_list[idx]["alignment"]["vertical"])
                            except:
                                cell.alignment = Alignment(horizontal="center", vertical="center")

                            try:    
                                cell.border = Border(top=activity_code_list[idx]["border"]["top"], 
                                                left=activity_code_list[idx]["border"]["left"], 
                                                right=activity_code_list[idx]["border"]["right"], 
                                                bottom=activity_code_list[idx]["border"]["bottom"])
                            except:
                                cell.border = Border(
                                    top=Side(border_style="thin", color="00000000"), 
                                    left=Side(border_style="thin", color="00000000"), 
                                    right=Side(border_style="thin", color="00000000"), 
                                    bottom=Side(border_style="thin", color="00000000"))
                                
                            try:
                                cell.fill = PatternFill(start_color=color_hex_list[idx]["value"], 
                                                        end_color=color_hex_list[idx]["value"], 
                                                        fill_type=color_hex_list[idx]["fill"]["fill_type"])
                            except:
                                color = color_hex_list[idx]["value"]
                                print(f"Color hex not found: {color}")
                                cell.fill = PatternFill(start_color=self.default_hex_fill_color, 
                                                        end_color=self.default_hex_fill_color, 
                                                        fill_type='solid')
                                
                            try:
                                cell.font = Font(name=activity_code_list[idx]["font"]["name"], 
                                            size=activity_code_list[idx]["font"]["size"], 
                                            bold=activity_code_list[idx]["font"]["bold"], 
                                            color=activity_code_list[idx]["font"]["color"])
                            except:
                                cell.font = Font(name="Calibri", size="12", bold=True, color=self.default_hex_font_color)

                            cell.value = activity_code_list[idx]["value"]
                            
                        break

        print("Workbook filled successfully.")


if __name__ == "__main__":
    ScheduleFramework.main(False)
