import os
import json
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string, get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.workbook.workbook import Workbook

class LegendsFramework():
    def __init__(self, input_excel_path, input_excel_basename, input_worksheet_name, input_json_path, 
                 input_json_basename, input_start_row, input_start_col):
        self.excel_path = input_excel_path
        self.excel_basename = input_excel_basename
        self.json_path = input_json_path
        self.json_basename = input_json_basename
        self.ws_name = input_worksheet_name
        self.start_row = int(input_start_row)
        self.start_col = str(input_start_col)
        self.wbs_start_row = 4
        self.wbs_start_col = 'A'
        self.default_hex_fill_color = "00FFFF00"

    @staticmethod
    def main():
        project = LegendsFramework.genrate_ins()
        active_workbook, active_worksheet = project.return_excel_workspace(project.ws_name)

        struct_dic = project.fashion_json()
        table = project.design_json_table()
        project.generate_legends_table(active_workbook, active_worksheet, table)

    @staticmethod
    def genrate_ins():
        input_excel_file = input("Please enter the path to the Excel file or directory: ")
        input_excel_path, input_excel_basename = LegendsFramework.file_verification(input_excel_file, 'e', 'f')
        input_worksheet_name = input("Please enter the name for the new or existing worksheet: ")
        input_start_row = input("Please enter the starting row to write the schedule: ")
        input_start_col = input("Please enter the starting column to write the schedule: ")
        input_json_file = input("Please enter the path to the Json file or directory: ")
        input_json_path, input_json_basename = LegendsFramework.file_verification(input_json_file, 'j', 'f')
        
        ins = LegendsFramework(input_excel_path, input_excel_basename, input_worksheet_name, 
                               input_json_path, input_json_basename, input_start_row, input_start_col)
        
        return ins

    @staticmethod
    def file_verification(input_file_path, file_type, mode):
        if os.path.isdir(input_file_path):
            path = input_file_path
            file = None

            if mode == 'f':
                dir_list = os.listdir(path)
                selection = LegendsFramework.display_directory_files(dir_list)
                base_name = dir_list[selection]
                print(f'File selected: {base_name}\n')
                file = os.path.join(path, base_name)
            elif mode == 's':
                base_name = None
                return path, base_name
            else:
                print("Error: Invalid mode specified.")
                return -1

            if (file_type == 'e' and LegendsFramework.is_xlsx(file)) or \
            (file_type == 'j' and LegendsFramework.is_json(file)):
                return path, base_name
            else:
                return -1
        elif os.path.isfile(input_file_path):
            if (file_type == 'e' and LegendsFramework.is_xlsx(input_file_path)) or \
            (file_type == 'j' and LegendsFramework.is_json(input_file_path)):
                path = os.path.dirname(input_file_path)
                base_name = os.path.basename(input_file_path)
                return path, base_name
            else:
                return -1
        else: 
            print('Error: Please verify that the directory and file exist and that the file is of type .xlsx or .json.')
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
                print('Error: Invalid input. Please enter a valid number.')

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
                    print(f"New worksheet '{worksheet_name}' created.")
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
                        print("Invalid selection. Returning without changes.")
                        return workbook, None
                        
                elif user_answer == 'q':
                    print("Quitting without changes.")
                    return workbook, None
                else:
                    print("Invalid input. Please enter 'Y' for Yes, 'N' for No, or 'Q' to Quit.")
        
        return workbook, worksheet
    
    def fashion_json(self):
        j_file = os.path.join(self.json_path, self.json_basename)

        with open(j_file, 'r') as json_file:
            data = json.load(json_file)
        
        df = self.flatten_json(data["project_content"][0])
        df_keys = list(df.keys())
        struct_dic = {}

        for key in df_keys:
            phase_key = key.split('|')[0]
            trade_key = key.split('|')[2]
            act_json_obj = {
                "entry": df[key].get("entry", None),
                "activity_code": df[key].get("activity_code", ""),
                "activity_name": df[key].get("activity_name", ""),
                "color": df[key].get("color", "")
            }

            if phase_key not in struct_dic:
                struct_dic[phase_key] = {}
            
            if trade_key not in struct_dic[phase_key]:
                struct_dic[phase_key][trade_key] = []

            struct_dic[phase_key][trade_key].append(act_json_obj)
        
        return struct_dic

    def design_json_table(self):
        j_file = os.path.join(self.json_path, self.json_basename)

        with open(j_file, 'r') as json_file:
            data = json.load(json_file)
        
        df = self.flatten_json(data["project_content"][0])
        df_keys = list(df.keys())
        struct_dic = []

        for key in df_keys:
            phase_key = key.split('|')[0]
            trade_key = key.split('|')[2]
            act_json_obj = {
                "phase": phase_key,
                "trade": trade_key,
                "entry": df[key].get("entry", None),
                "activity_code": df[key].get("activity_code", ""),
                "activity_name": df[key].get("activity_name", ""),
                "color": df[key].get("color", "")
            }

            struct_dic.append(act_json_obj)
        
        df_table = pd.DataFrame(struct_dic)

        return df_table
    
    def generate_legends_table(self, active_wb, active_ws, og_table):
        wb = active_wb
        ws = active_ws
        file = os.path.join(self.excel_path, self.excel_basename)
        
        proc_table = pd.pivot_table(
            og_table,
            index=["phase", "trade", "activity_code", "color"],
            values="activity_name",
            aggfunc='first'
        )
        """                                      
        phase   trade   activity_code    activity_name
        Phase 1 Trade 1 1A               Activity 1
                        1B               Activity 2
                        1C               Activity 3
                        1D               Activity 4
                        1E               Activity 5
                Trade 2 2A               Activity 1
                        2B               Activity 2
                        2C               Activity 3
                        2D               Activity 4
                        2E               Activity 5
        Phase 2 Trade 1 1A               Activity 1
                        1B               Activity 2 """
        current_row = self.start_row
        current_col = column_index_from_string(self.start_col)
        current_phase = None
        current_trade = None
        counter = 0

        for (phase, trade, activity_code, color) in proc_table.index:
            if counter == 0:
                if phase != current_phase:
                    current_row = self.start_row
                    self.style_cell(ws, current_row, current_col, phase, "00800080")
                    ws.merge_cells(start_row=current_row, 
                                   start_column=current_col, 
                                   end_row=current_row, 
                                   end_column=current_col + 1)
                    current_phase = phase
                    current_row += 1 

                if trade != current_trade:
                    current_row += 1 
                    self.style_cell(ws, current_row, current_col, trade, self.process_hex_val(color))
                    ws.merge_cells(start_row=current_row, 
                                   start_column=current_col, 
                                   end_row=current_row, 
                                   end_column=current_col + 1)
                    current_trade = trade  
                    current_row += 1 

                self.style_cell(ws, current_row, current_col, activity_code, self.process_hex_val(color))                
                self.style_cell(ws, current_row, current_col + 1, proc_table.loc[(phase, trade, activity_code, color)].values[0] , "00FFFFFF")

                current_row += 1  
            else:
                if phase != current_phase:
                    current_col += 3
                    current_row = self.start_row
                    self.style_cell(ws, current_row, current_col, phase, "00800080")
                    ws.merge_cells(start_row=current_row, 
                                   start_column=current_col, 
                                   end_row=current_row, 
                                   end_column=current_col + 1)
                    current_phase = phase
                    current_row += 1 

                if trade != current_trade:
                    current_row += 1 
                    self.style_cell(ws, current_row, current_col, trade, self.process_hex_val(color))
                    ws.merge_cells(start_row=current_row, 
                                   start_column=current_col, 
                                   end_row=current_row, 
                                   end_column=current_col + 1)
                    current_trade = trade  
                    current_row += 1

                self.style_cell(ws, current_row, current_col, activity_code, self.process_hex_val(color))
                self.style_cell(ws, current_row, current_col + 1, proc_table.loc[(phase, trade, activity_code, color)].values[0] , "00FFFFFF")

                current_row += 1      

            counter +=1        

        wb.save(filename=file)
        print("Legends table generated successfully.")

    def process_hex_val(self, hex_val):
        if '#' in hex_val:
            hex_val = hex_val.replace('#', "00")

        if len(hex_val) != 8:
            print(f"Error: Invalid hex value '{hex_val}'. Hex values must be 6 characters long.")
            return self.default_hex_fill_color

        return hex_val

    def style_cell(self, active_ws, current_row, current_col, val, color_hex):
        ws = active_ws
        try:
            cell = ws.cell(row=current_row, 
                            column=current_col, 
                            value=val)
            cell.alignment = Alignment(horizontal="center", 
                                        vertical="center")
            cell.fill = PatternFill(start_color=color_hex, 
                                    end_color=color_hex, 
                                    fill_type="solid")
            cell.font = Font(name="Calibri", 
                            size="12", 
                            bold=True, 
                            color="00000000")
            cell.border = Border(left=Side(border_style="thin", color="00000000"),
                                right=Side(border_style="thin", color="00000000"),
                                top=Side(border_style="thin", color="00000000"),
                                bottom=Side(border_style="thin", color="00000000"))
        except KeyError as e:
            print(f"Error styling cell at row {current_row}, column {current_col}: {e}")

    def generate_legends_frame(self, table):
        excel_file = os.path.join(self.excel_path, self.excel_basename)

        if isinstance(table, pd.DataFrame) and not table.empty:
            with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists="overlay") as writer:
                table.to_excel(writer, sheet_name=self.ws_name, index=False,
                            startrow=self.start_row - 1,
                            startcol=column_index_from_string(self.start_col) - 1)

            print(f"Successfully converted JSON to Excel and saved to {excel_file}")
        else:
            print("The provided table is not a valid DataFrame or is empty.")

    def generate_data_frame(self, struct_dic):
        temp_list = []
        final_list = []

        for key, val in struct_dic.items():
            current_phase = key
            legend_table_header = {
                "phase": key,
                "trades": []
            }

            for trade in val:
                act_list = struct_dic[current_phase][trade]
                legend_table_body = [{
                    "trade": trade,
                    "activity_code": activity["activity_code"],
                    "activity_name": activity["activity_name"],
                } for activity in act_list]

                legend_table_header["trades"].append(legend_table_body)
            
            temp_list.append(legend_table_header)
            
            
        df = pd.DataFrame(temp_list)
        pvt_df = df.pivot_table(columns="phase", values="trades", aggfunc='first')
        print(pvt_df)

    def write_data_to_excel(self, flatten_dic, sheet_name):
        e_file = os.path.join(self.excel_path, self.excel_basename)
        flatten_df = pd.DataFrame(flatten_dic)
        print(flatten_df)

        try:
            with pd.ExcelWriter(e_file, engine='openpyxl', mode='w') as writer:
                flatten_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=3)

            print(f"Data successfully written to {sheet_name} in {self.filled_excel_path}.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

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


if __name__ == "__main__":
    LegendsFramework.main()
