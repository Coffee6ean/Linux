import os
import json
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string, get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.workbook.workbook import Workbook

class WbsFramework:
    def __init__(self, input_process_cont, input_excel_path, input_excel_basename, 
                input_worksheet_name, input_json_path, input_json_basename):
        self.process_cont = input_process_cont
        self.excel_path = input_excel_path
        self.excel_basename = input_excel_basename
        self.ws_name = input_worksheet_name
        self.json_path = input_json_path
        self.json_basename = input_json_basename
    
    @staticmethod
    def main():
        project = WbsFramework.generate_ins()
        table = project.design_json_table()
        project.generate_wbs_cfa_style(table)

    @staticmethod
    def generate_ins():
        input_process_cont = WbsFramework.ynq_user_interaction("Continue with the program? ")
        if input_process_cont == 'q':
            print("Exiting the program.")
            return -1 
        
        input_excel_file = input("Please enter the path to the Excel file or directory: ")
        input_worksheet_name = input("Please enter the name for the new or existing worksheet: ")
        input_json_file = input("Please enter the path to the Json file or directory: ")

        input_excel_path, input_excel_basename = WbsFramework.file_verification(
            input_excel_file, 'e', 'c')
        input_json_path, input_json_basename = WbsFramework.file_verification(
                input_json_file, 'j', 'r')

        ins = WbsFramework(input_process_cont, input_excel_path, input_excel_basename, 
                            input_worksheet_name, input_json_path, input_json_basename)
        
        return ins

    @staticmethod
    def ynq_user_interaction(prompt_message):
        valid_responses = {'y', 'n', 'q'}  
        
        while True:
            user_input = input(prompt_message).lower()  
            
            if user_input in valid_responses:
                return user_input  
            else:
                print("Error. Invalid input, please try again. ['Y/y' for Yes, 'N/n' for No, 'Q/q' for Quit]\n")

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
        if file_name.endswith(".xlsx"):
            return True
        else:
            print("Error. Selected file is not an Excel")
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

            if mode == 'u' or mode == 'r' or mode == 'd':
                dir_list = os.listdir(path)
                selection = WbsFramework.display_directory_files(dir_list)
                base_name = dir_list[selection]
                print(f'File selected: {base_name}\n')
                file = os.path.join(path, base_name)
            elif mode == 'c':
                base_name = None
                return path, base_name
            else:
                print("Error: Invalid mode specified.")
                return -1

            if (file_type == 'e' and WbsFramework.is_xlsx(file)) or \
            (file_type == 'j' and WbsFramework.is_json(file)):
                return path, base_name
            else:
                return -1
        elif os.path.isfile(input_file_path):
            if (file_type == 'e' and WbsFramework.is_xlsx(input_file_path)) or \
            (file_type == 'j' and WbsFramework.is_json(input_file_path)):
                path = os.path.dirname(input_file_path)
                base_name = os.path.basename(input_file_path)
                return path, base_name
            else:
                return -1
        else: 
            print("Error: Please verify that the directory and file exist and that the file is of type .xlsx or .json.")
            return -1
    
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
                    selected_ws_idx = WbsFramework.display_directory_files(ws_list)
                    
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

    def design_json_table(self):
        j_file = os.path.join(self.json_path, self.json_basename)

        with open(j_file, 'r') as json_file:
            data = json.load(json_file)
        
        df = self.flatten_json(data["project_content"][0])
        df_keys = list(df.keys())
        struct_dic = []

        for key in df_keys:
            phase_key = key.split('|')[0]
            location_key = key.split('|')[1]
            act_json_obj = {
                "phase": phase_key,
                "location": location_key,
                "entry": df[key].get("entry", None),
                "activity_code": df[key].get("activity_code", ""),
                "activity_name": df[key].get("activity_name", ""),
                "color": df[key].get("color", ""),
                "start": df[key].get("start", ""),
                "finish": df[key].get("finish", "")
            }

            struct_dic.append(act_json_obj)
        
        df_table = pd.DataFrame(struct_dic)

        return df_table

    def generate_wbs_cfa_style(self, og_table):
        proc_table = pd.pivot_table(
            og_table,
            index=["phase", "location", "activity_code", "color", "entry"],
            values=["start", "finish"],
            aggfunc='first'
        )
        """                                                              
        phase              location activity_code color    finish     start
        Interior Finishes  Zone 1   APL-A2        #FF99FF  10-Oct-24  27-Sep-24
                                    APL-A3        #FF99FF  06-Nov-24  24-Oct-24
                                    CLN-C2        #FF6600  06-Nov-24  24-Oct-24
                                    CSE-71        #0070C0  26-Sep-24  13-Sep-24
                                    DRS-51        #FDE9D9  17-Sep-24  13-Sep-24
        ...                                                      ...        ...
        Interior Rough Ins Zone 4   PLM-43        #99CC00  08-Oct-24  02-Oct-24
                                    PLM-47        #99CC00  01-Oct-24  11-Sep-24
                                    PTG-60        #CCFFFF  08-Oct-24  07-Oct-24
                                    PTG-61        #CCFFFF  08-Oct-24  02-Oct-24
                                    PTG-63        #CCFFFF  13-Nov-24  07-Nov-24 """
        print(proc_table)

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
    WbsFramework.main()