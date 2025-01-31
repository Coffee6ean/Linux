import os
import re
import json
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string, get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

# Imported Helper - As Module
""" from .setup import Setup """

# Imported Helper - As Package 
from modules.setup import Setup

class LegendsFramework():
    def __init__(self, input_file_path, input_file_basename, input_file_extension, 
                 input_worksheet_name, project_table, input_start_row=1, input_start_col='A'):
        self.input_path = input_file_path
        self.input_basename = input_file_basename
        self.input_extension = input_file_extension
        self.worksheet_name = input_worksheet_name
        self.table = project_table

        #Module Attributes
        self.start_row = int(input_start_row)
        self.start_col = str(input_start_col)
        self.default_hex_fill_color = "00FFFF00"
        self.dark_default_hex_font = "00000000"
        self.light_default_hex_font = "00FFFFFF"

    @staticmethod
    def main(auto=True, input_file_path=None, input_file_basename=None, 
             input_file_extension=None, input_worksheet_name=None, project_table=None):
        if auto:
            project = LegendsFramework.auto_generate_ins(
                input_file_path, 
                input_file_basename, 
                input_file_extension,
                input_worksheet_name, 
                project_table,
            )
        else:
            project = LegendsFramework.generate_ins()
        
        active_workbook, active_worksheet = project.return_excel_workspace(project.worksheet_name)

        if active_workbook and active_worksheet:
            project.generate_legends_table(
                active_workbook, 
                active_worksheet, 
                project.table.reset_index()
            )

    @staticmethod
    def generate_ins():
        LegendsFramework.ynq_user_interaction(
            "Run as Module as stand-alone? "
        )

        setup = Setup.main()

        project_ins_dict = {"setup": setup.obj}
        ins = LegendsFramework(project_ins_dict)

        return ins

    @staticmethod
    def auto_generate_ins(input_file_path, input_file_basename, input_file_extension, 
                          input_worksheet_name, project_table):
        ins = LegendsFramework(
            input_file_path, 
            input_file_basename, 
            input_file_extension,
            input_worksheet_name, 
            project_table,
        )
        
        return ins

    @staticmethod
    def ynq_user_interaction(prompt_message):
        valid_responses = {'y', 'n', 'q'}  
        
        while True:
            user_input = input(prompt_message).lower().strip()
            
            if user_input in valid_responses:
                return user_input  
            else:
                print("Error. Invalid input, please try again. ['Y/y' for Yes, 'N/n' for No, 'Q/q' for Quit]\n")

    @staticmethod
    def file_verification(input_file_path, file_type, mode, input_json_title=None):
        if input_json_title and os.path.isdir(input_file_path):
            file_basename = f"processed_{LegendsFramework.normalize_entry(input_json_title)}.json"
            path, basename = LegendsFramework.handle_file(input_file_path, file_basename, file_type)
        else:
            if os.path.isdir(input_file_path):
                file_path, file_basename = LegendsFramework.handle_dir(input_file_path, mode)
                if mode != 'c':
                    path, basename = LegendsFramework.handle_file(file_path, file_basename, file_type)
                else:
                    path = file_path
                    basename = file_basename
            elif os.path.isfile(input_file_path):
                file_path = os.path.dirname(input_file_path)
                file_basename = os.path.basename(input_file_path)
                path, basename = LegendsFramework.handle_file(file_path, file_basename, file_type)

        return path, basename
    
    @staticmethod
    def handle_dir(input_path, mode):
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_path)
            selection = LegendsFramework.display_directory_files(dir_list)
            base_name = dir_list[selection]
            print(f'File selected: {base_name}\n')
        elif mode == 'c':
            base_name = None
        else:
            print("Error: Invalid mode specified.\n")
            return -1
        
        return input_path, base_name

    @staticmethod
    def handle_file(file_path, file_basename, file_type):
        file = os.path.join(file_path, file_basename)

        if (file_type == 'e' and LegendsFramework.is_xlsx(file)) or \
           (file_type == 'j' and LegendsFramework.is_json(file)):
            return os.path.dirname(file), os.path.basename(file)
        
        print("Error: Please verify that the directory and file exist and that the file is of type .xlsx or .json")
        return -1
    
    @staticmethod
    def display_directory_files(file_list):
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
    def hex2rgb(hex_color):
        trimmed_hex = hex_color.lstrip('#')
        calc_rgb = tuple(int(trimmed_hex[i:i+2], 16) for i in (0, 2, 4))

        return calc_rgb

    @staticmethod
    def calculateLuminance(R, G, B):
        lum = 0.2126*(R/255.0)**2.2 + 0.7152*(G/255.0)**2.2 + 0.0722*(B/255.0)**2.2

        return lum

    @staticmethod
    def normalize_entry(entry_str):
        remove_bewteen_parenthesis = re.sub('(?<=\()(.*?)(?=\))', '', entry_str)
        special_chars = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        remove_special_chars = re.sub(special_chars, '', remove_bewteen_parenthesis.lower())
        normalized_str = re.sub(' ', '_', remove_special_chars)

        return normalized_str

    def return_excel_workspace(self, worksheet_name):
        basename = self.input_basename + '.' + self.input_extension
        file = os.path.join(self.input_path, basename)
        
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
                    print(f"New worksheet '{worksheet_name}' created.\n")
                    break
                elif user_answer == 'n':
                    ws_list = workbook.sheetnames
                    selected_ws_idx = LegendsFramework.display_directory_files(ws_list)
                    
                    if selected_ws_idx >= 0:  
                        worksheet = workbook.worksheets[selected_ws_idx]
                        self.ws_name = ws_list[selected_ws_idx]
                        print(f"Worksheet selected: '{self.ws_name}'")
                        return workbook, worksheet
                    else:
                        print("Invalid selection. Returning without changes.\n")
                        return workbook, None
                        
                elif user_answer == 'q':
                    print("Quitting without changes.\n")
                    return workbook, None
                else:
                    print("Invalid input. Please enter 'Y' for Yes, 'N' for No, or 'Q' to Quit.")
        
        return workbook, worksheet

    def generate_legends_table(self, active_wb, active_ws, og_table):
        basename = self.input_basename + '.' + self.input_extension
        file = os.path.join(self.input_path, basename)
        wb = active_wb
        ws = active_ws

        proc_table = pd.pivot_table(
            og_table.reset_index(),
            index=["phase", "trade", "color"],
            values=["activity_name", "activity_code"],
            aggfunc={
                "activity_name": "first",
                "activity_code": "first"
            },
            observed=True
        )

        column_width_dict = self.define_column_width(proc_table)
        reset_table = proc_table.reset_index()

        current_row = self.start_row
        current_col = column_index_from_string(self.start_col)
        current_phase = None
        current_trade = None
        counter = 0

        for index, row in reset_table.iterrows():
            phase = row['phase']
            trade = row['trade']
            color = row['color']
            activity_code = row['activity_code']
            activity_name = row['activity_name']

            if counter == 0:
                if phase != current_phase:
                    current_row = self.start_row
                    self._style_cell(
                        ws, 
                        current_row, 
                        current_col, 
                        phase, 
                        "00800080", 
                        "center",
                        column_width_dict[phase].get("name")
                    )
                    ws.merge_cells(
                        start_row=current_row, 
                        start_column=current_col, 
                        end_row=current_row, 
                        end_column=current_col + 1
                    )
                    current_phase = phase
                    current_row += 1 

                if trade != current_trade:
                    current_row += 1 
                    self._style_cell(
                        ws, 
                        current_row, 
                        current_col, 
                        trade, 
                        self.process_hex_val(color), 
                        "center",
                        column_width_dict[phase].get("name")
                    )
                    ws.merge_cells(
                        start_row=current_row, 
                        start_column=current_col, 
                        end_row=current_row, 
                        end_column=current_col + 1
                    )
                    current_trade = trade  
                    current_row += 1 

                self._style_cell(
                    ws, 
                    current_row, 
                    current_col, 
                    activity_code, 
                    self.process_hex_val(color), 
                    "center",
                    column_width_dict[phase].get("code")
                )                
                self._style_cell(
                    ws, 
                    current_row, 
                    current_col + 1, 
                    activity_name, 
                    "00FFFFFF",
                    "left",
                    column_width_dict[phase].get("name")
                )

                current_row += 1  
            else:
                if phase != current_phase:
                    current_col += 3
                    current_row = self.start_row
                    self._style_cell(
                        ws, 
                        current_row, 
                        current_col, 
                        phase, 
                        "00800080", 
                        "center",
                        column_width_dict[phase].get("name")
                    )
                    ws.merge_cells(
                        start_row=current_row, 
                        start_column=current_col, 
                        end_row=current_row, 
                        end_column=current_col + 1
                    )
                    current_phase = phase
                    current_row += 1 

                if trade != current_trade:
                    current_row += 1 
                    self._style_cell(
                        ws, 
                        current_row, 
                        current_col, 
                        trade, 
                        self.process_hex_val(color),
                        "center",
                        column_width_dict[phase].get("name")
                    )
                    ws.merge_cells(start_row=current_row, 
                                   start_column=current_col, 
                                   end_row=current_row, 
                                   end_column=current_col + 1)
                    current_trade = trade  
                    current_row += 1

                self._style_cell(
                    ws, 
                    current_row, 
                    current_col, 
                    activity_code, 
                    self.process_hex_val(color),
                    "center",
                    column_width_dict[phase].get("code")
                )
                self._style_cell(
                    ws, 
                    current_row, 
                    current_col + 1, 
                    activity_name, 
                    "00FFFFFF",
                    "left",
                    column_width_dict[phase].get("name")
                )

                current_row += 1      

            counter +=1        

        wb.save(filename=file)
        print("Legends table generated successfully.")

    def define_column_width(self, proc_table):
        phase_widths = {}

        for phase, group in proc_table.groupby(level="phase", observed=True):
            max_length_code = max(len(str(activity)) for activity in group["activity_code"].dropna())
            max_length_name = max(len(str(activity)) for activity in group["activity_name"].dropna())
            phase_widths[phase] = dict(
                code = max_length_code + 2,
                name = max_length_name + 2,
            )

        return phase_widths

    def process_hex_val(self, hex_val):
        if '#' in hex_val:
            hex_val = hex_val.replace('#', "00")

        if len(hex_val) != 8:
            print(f"Error: Invalid hex value '{hex_val}'. Hex values must be 6 characters long.\n")
            return self.default_hex_fill_color

        return hex_val

    def _style_cell(self, active_ws, current_row, current_col, val, 
                    color_hex, horz_alignment, cell_width=50):
        ws = active_ws
        try:
            cell = ws.cell(row=current_row, 
                            column=current_col, 
                            value=val)
            cell.alignment = Alignment(horizontal=horz_alignment, 
                                        vertical="center")
            
            cell.border = Border(left=Side(border_style="thin", color="00000000"),
                                right=Side(border_style="thin", color="00000000"),
                                top=Side(border_style="thin", color="00000000"),
                                bottom=Side(border_style="thin", color="00000000"))

            cell.fill = PatternFill(start_color=color_hex, 
                                    end_color=color_hex, 
                                    fill_type="solid")
            
            rgb = LegendsFramework.hex2rgb(color_hex)
            lum_rgb = LegendsFramework.calculateLuminance(rgb[0], rgb[1], rgb[2])

            if lum_rgb > 0.5:
                cell.font = Font(name="Calibri", size="12", bold=True, color=self.dark_default_hex_font)
            else:
                cell.font = Font(name="Calibri", size="12", bold=True, color=self.light_default_hex_font)

            ws.column_dimensions[get_column_letter(cell.column)].width = cell_width
        except KeyError as e:
            print(f"Error styling cell at row {current_row}, column {current_col}: {e}")


if __name__ == "__main__":
    LegendsFramework.main(False)
