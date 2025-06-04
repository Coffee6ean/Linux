import os
import json
import pandas as pd
from datetime import datetime
from openpyxl.utils import column_index_from_string

#LLM
from ollama import Client

import sys
sys.path.append("../")
from CpmProcessor.keys.secrets import TEST_XLSX_DIR
from CpmProcessor.keys.secrets import DICT_TPS_SYSTEM, LLM_MODEL

class PdfDataProcessing():
    allowed_extensions = ["json", "xlsx"]

    def __init__(self, input_file_path, input_file_basename, 
                 input_file_extension, project_data_dict):
        #Module Attribuates
        self.file_path = input_file_path
        self.file_basename = input_file_basename
        self.file_extension = input_file_extension
        self.data_dict = project_data_dict
    
    @staticmethod
    def main(auto=True, input_file_path=None, input_file_basename=None, 
             input_file_extension=None, project_data_dict=None):
        if auto:
            project = PdfDataProcessing.auto_generate_ins(
                input_file_path, 
                input_file_basename, 
                input_file_extension, 
                project_data_dict
            )
        else:
            project = PdfDataProcessing.generate_ins()

        module_data = {
            "details": {
                "workbook": None,
                "worksheet": None,
                "df_rows": 0,
            },
            "logs": {
                "start": PdfDataProcessing.return_valid_date(),
                "finish": None,
                "run-time": None,
                "status": [],
            },
            "content": {}
        }

        if project:
            table = project.tabulate_data(project.data_dict)
            PdfDataProcessing.write_df_to_excel(
                table, 
                "project_table", 
                "cpm_wbs_table", 
                1, 
                "A"
            )
            module_data["details"]["df_rows"] = table.shape[0] + 1
            module_data["content"] = table

        module_data["logs"]["finish"] = PdfDataProcessing.return_valid_date()
        module_data["logs"]["run-time"] = PdfDataProcessing.calculate_time_duration(
            module_data["logs"].get("start"), 
            module_data["logs"].get("finish")
        )

        return module_data

    @staticmethod
    def generate_ins():
        input_file = PdfDataProcessing.return_valid_file(
            input("Please enter the path to the file or directory: ").strip()
        )

        ins = PdfDataProcessing(
            input_file.get("path"), 
            input_file.get("basename"), 
            input_file.get("extension"),
            PdfDataProcessing.read_data_from_json(
                input_file.get("path"), 
                input_file.get("basename")
            ),
        )

        return ins

    @staticmethod
    def auto_generate_ins(input_file_path, input_file_basename, 
                          input_file_extension, project_data_dict):
        ins = PdfDataProcessing(
            input_file_path, 
            input_file_basename, 
            input_file_extension,
            project_data_dict
        )

        return ins

    @staticmethod
    def return_valid_file(input_file_dir:str) -> dict|int:
        if not os.path.exists(input_file_dir):
            raise FileNotFoundError("Error: Given directory or file does not exist in the system.")

        if os.path.isdir(input_file_dir):
            file_dict = PdfDataProcessing._handle_dir(input_file_dir)
        elif os.path.isfile(input_file_dir):
            file_dict = PdfDataProcessing._handle_file(input_file_dir)

        return file_dict
    
    @staticmethod
    def _handle_dir(input_file_dir:str, mode:str="r") -> dict|int:
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_file_dir)
            selection = PdfDataProcessing._display_directory_files(dir_list)
            input_file_basename = dir_list[selection]
            print(f'File selected: {input_file_basename}\n')
        elif mode == 'c':
            input_file_basename = None
        else:
            print("Error: Invalid mode specified.")
            return -1
        
        return dict(
            path = os.path.dirname(input_file_dir), 
            basename = os.path.basename(input_file_basename).split(".")[0],
            extension = os.path.basename(input_file_basename).split(".")[-1],
        )
    
    @staticmethod
    def _display_directory_files(file_list:list) -> int:
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
    def _handle_file(input_file_dir:str) -> dict|int:
        input_file_extension = os.path.basename(input_file_dir).split(".")[-1]

        if (input_file_extension in PdfDataProcessing.allowed_extensions):
            return dict(
                path = os.path.dirname(input_file_dir), 
                basename = os.path.basename(input_file_dir).split(".")[0],
                extension = input_file_extension,
            )

        print("Error: Please verify that the directory and file exist and that the file extension complies with class attributes")
        return -1

    @staticmethod
    def return_valid_date() -> str:
        now = datetime.now()
        date_str = now.strftime("%d-%b-%y %H:%M:%S")

        return date_str

    @staticmethod
    def calculate_time_duration(start_date:str, finish_date:str, 
                                date_format:str="%d-%b-%y %H:%M:%S") -> float|int:
        try:
            start_time = datetime.strptime(start_date, date_format)
            finish_time = datetime.strptime(finish_date, date_format)

            minutes_duration = (finish_time - start_time).total_seconds()

            return minutes_duration
        except (ValueError, TypeError) as e:
            print(f"Error calculating runtime: {e}")
            return -1

    @staticmethod
    def read_data_from_json(file_path:str, file_basename:str, file_extension:str="json"):
        basename = f"{file_basename}.{file_extension}"
        file = os.path.join(file_path, basename)
        
        with open(file, 'r') as json_file:
            data = json.load(json_file)

        return data

    @staticmethod
    def write_df_to_excel(table, file_name:str, ws_name:str, 
                          wbs_start_row:int, wbs_start_col:str) -> None:
        if table.empty:
            print("Error: DataFrame is empty. No data to write.\n")
            return
        
        new_directory = f"{TEST_XLSX_DIR}/{PdfDataProcessing.return_valid_date()}"
        os.makedirs(new_directory, exist_ok=True)

        basename = file_name.split(".")[0] if "." in file_name else file_name
        new_file = os.path.join(new_directory, f"{basename}.xlsx")

        try:
            with pd.ExcelWriter(new_file, engine="openpyxl", mode='w') as writer:
                table.to_excel(
                    writer,
                    sheet_name=ws_name,
                    startrow=wbs_start_row - 1,
                    startcol=column_index_from_string(wbs_start_col) - 1
                )

            print(f"Successfully saved DataFrame to Excel:\nFile: {new_directory}\nSheet: {ws_name}\n")
        except Exception as e:
            print(f"An unexpected error occurred while writing to Excel: {e}\n")

    def tabulate_data(self, data_dict:dict):
        with open(DICT_TPS_SYSTEM, 'r') as json_file:
            framework = json.load(json_file)

        phases = list(framework.keys())
        project_valid_tasks = []
        
        for key, value in data_dict.items():
            tasks = [{
                "phase": self._calculate_phase(entry.get("parent_name"), phases),
                "area": "",
                "zone": "",
                "trade": "",
                "color": "",
                "parent_page": int(key),
                "parent_entry": entry.get("entry"),
                "parent_id": entry.get("parent_id"),
                "parent_name": entry.get("parent_name"),
                "parent_start": entry.get("parent_start"),
                "parent_finish": entry.get("parent_finish")
            } for entry in value["body"]["content"]]

            project_valid_tasks.extend(tasks)

        df_table = pd.DataFrame(project_valid_tasks)
        df_table.fillna("", inplace=True)

        return df_table

    def _calculate_phase(self, task_name:str, phases:list):
        selected_phase = self._complete_project(task_name, phases)
        print(selected_phase)

        return selected_phase

    def _calculate_trade(self, task_name:str, trades:list):
        selected_trade = self._complete_project(task_name, trades)

        return selected_trade

    def _complete_project(self, task:str, options:list):
        selection = self._call_ollama(
            f"""
            Chat - determine the best phase for this activity '{task}', 
            out of this list: {options}. Just give me the option, no explanation or reasoning needed.
            """,
            LLM_MODEL
        )

        return selection

    def _call_ollama(self, prompt:str, llm_model:str="llama2") -> str:
        try:
            client = Client(
                host='http://localhost:11434',
                headers={'x-some-header': 'some-value'}
            )
            response = client.chat(model=llm_model, messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])
        except Exception as e:
            print(f"Error during Ollama API call: {e}")
            return None

        return response['message']['content']


if __name__ == "__main__":
    PdfDataProcessing.main(False)
        