import os
import json
import pandas as pd
from datetime import datetime, timedelta
from openpyxl.utils import column_index_from_string

import sys
sys.path.append("../")
from backend.config.paths import TEST_XLSX_DIR, TEST_PDF_DIR

class DataFrameSetup:
    allowed_extensions = ["json"]

    def __init__(self, input_file_path, input_file_basename, 
                 input_file_extension, output_file_dir, project_data):
        self.input_path = input_file_path
        self.input_basename = input_file_basename
        self.input_extension = input_file_extension
        self.output_path = output_file_dir
        self.project_data = project_data

        #Structures
        self.json_struct_categories = ["phase", "area", "zone", "subzone", "level", "trade", "activity_code"]
        self.custom_phase_order = ["procurement", "milestone"]
        self.project_table_index = ["phase", "area", "zone", "subzone", "level", "entry", "activity_code"]
        self.project_table_values = ["trade", "color", "activity_name", "start", "finish"]
        self.wbs_final_categories = ["phase", "area", "zone", "subzone", "level"]

    @staticmethod
    def main(auto=True, input_file_path=None, input_file_basename=None, 
             input_file_extension=None, output_file_dir=None, project_data=None):
        if auto:
            project = DataFrameSetup.auto_generate_ins(
                input_file_path, 
                input_file_basename, 
                input_file_extension, 
                output_file_dir,
                project_data
            )
        else:
            project = DataFrameSetup.generate_ins()

        module_data = {
            "details": {
                "json": None,
                "df_rows": 0,
            },
            "logs": {
                "start": DataFrameSetup.return_valid_date(),
                "finish": None,
                "run-time": None,
                "status": [],
            },
            "content": {}
        }

        if project:
            if project.project_data:
                content = project.setup_project(project.project_data["body"])
                module_data["details"]["df_rows"] = content["table"].shape[0] + 1
                module_data["content"] = content
            else:
                if project.input_extension in DataFrameSetup.allowed_extensions:
                    content = project.setup_project(project.project_data)
                    module_data["details"] = content["table"].shape[0]
                    module_data["content"] = content
                else:
                    print("Error. Unsuported file type")
                    module_data["logs"]["status"].append(dict(
                        Error=f"{DataFrameSetup.__name__}| Unsuported input file extension: {project.input_extension}"
                    ))
        else:
            module_data["logs"]["status"].append(dict(
                Error= f"{DataFrameSetup.__name__}| Module's instance was not generated correctly"
            ))

        module_data["logs"]["finish"] = DataFrameSetup.return_valid_date()
        module_data["logs"]["run-time"] = DataFrameSetup.calculate_time_duration(
            module_data["logs"].get("start"), 
            module_data["logs"].get("finish")
        )
        module_data["logs"]["status"].append(dict(
            Info=f"{DataFrameSetup.__name__}| Module ran successfully"
        ))

        return module_data

    @staticmethod
    def generate_ins():
        input_file = DataFrameSetup.return_valid_file(
            input("Please enter the path to the file or directory: ").strip()
        )
        output_file_dir = DataFrameSetup.return_valid_path(
            "Please enter the directory to save the new module results: "
        )

        ins = DataFrameSetup(
            input_file.get("path"), 
            input_file.get("basename"),
            input_file.get("extension"),
            output_file_dir,
            None
        )
        
        return ins

    @staticmethod
    def auto_generate_ins(input_file_path, input_file_basename, 
                          input_file_extension, output_file_dir, project_data):
        ins = DataFrameSetup(
            input_file_path, 
            input_file_basename, 
            input_file_extension, 
            output_file_dir,
            project_data
        )
        
        return ins

    @staticmethod
    def clear_directory(directory_path:str) -> None:
        if os.path.isdir(directory_path):
            file_list = os.listdir(directory_path)
            for file in file_list:
                file_path = os.path.join(directory_path, file)
                os.remove(file_path)

    @staticmethod
    def return_valid_file(input_file_dir:str) -> dict|int:
        if not os.path.exists(input_file_dir):
            raise FileNotFoundError("Error: Given directory or file does not exist in the system.")

        if os.path.isdir(input_file_dir):
            file_dict = DataFrameSetup._handle_dir(input_file_dir)
        elif os.path.isfile(input_file_dir):
            file_dict = DataFrameSetup._handle_file(input_file_dir)

        return file_dict
    
    @staticmethod
    def _handle_dir(input_file_dir:str, mode:str="r") -> dict|int:
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_file_dir)
            selection = DataFrameSetup._display_directory_files(dir_list)
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
    def _handle_file(input_file_dir:str):
        input_file_extension = os.path.basename(input_file_dir).split(".")[-1]

        if (input_file_extension in DataFrameSetup.allowed_extensions):
            return dict(
                path = os.path.dirname(input_file_dir), 
                basename = os.path.basename(input_file_dir).split(".")[0],
                extension = input_file_extension,
            )

        print("Error: Please verify that the directory and file exist and that the file extension complies with class attributes")
        return -1
    
    @staticmethod
    def return_valid_path(prompt_message:str) -> (str|None):
        while(True):   
            value = input(prompt_message).strip()
            try:
                if os.path.isdir(value):
                    return value
            except Exception as e:
                print(f"Error. {e}\n")

    @staticmethod
    def return_valid_date() -> str:
        now = datetime.now()
        date_str = now.strftime("%d-%b-%y %H:%M:%S")

        return date_str

    @staticmethod
    def add_date() -> str:
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

        return dt_string

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
    def write_df_to_excel(proc_table, file_name:str, 
                          ws_name:str, wbs_start_row:int, wbs_start_col:str) -> None:
        if proc_table.empty:
            print("Error: DataFrame is empty. No data to write.\n")
            return

        base_name = file_name.split(".")[0] if "." in file_name else file_name
        new_directory = os.path.join(TEST_XLSX_DIR, base_name)

        os.makedirs(new_directory, exist_ok=True)

        file_path = os.path.join(new_directory, f"{DataFrameSetup.add_date()}.xlsx")

        try:
            with pd.ExcelWriter(file_path, engine="openpyxl", mode='w') as writer:
                proc_table.to_excel(
                    writer,
                    sheet_name=ws_name,
                    startrow=wbs_start_row - 1,
                    startcol=column_index_from_string(wbs_start_col) - 1
                )

            print(f"Successfully saved DataFrame to Excel:\nFile: {file_path}\nSheet: {ws_name}\n")
        except Exception as e:
            print(f"An unexpected error occurred while writing to Excel: {e}\n")

    def setup_project(self, data:dict=None) -> dict:
        if not data:
            flat_json_obj = self.read_json_obj()
        else:
            df = self._flatten_json(data)
            flat_json_obj = list(df.values())

        table, custom_ordered_dict, custom_phase_order = self.design_json_table(flat_json_obj)
        proc_table = self.generate_wbs_cfa_style(table, custom_phase_order, "phase")
        lead_schedule_struct = self.determine_schedule_structure(custom_ordered_dict)

        content = {
            "table": proc_table,
            "custom_ordered_dict": custom_ordered_dict,
            "custom_phase_order": custom_phase_order,
            "lead_schedule_struct": lead_schedule_struct
        }

        return content

    def read_json_obj(self) -> list:
        j_file = os.path.join(self.input_path, self.input_basename)

        with open(j_file, 'r') as json_file:
            data = json.load(json_file)
        
        df = self._flatten_json(data["body"])
        df_values = list(df.values())

        return df_values
    
    def _flatten_json(self, json_obj:dict) -> dict:
        new_dic = {}

        def flatten(obj:dict, flattened_key:str=""):
            if type(obj) is dict:
                keys_in_dic = list(obj.keys())

                if "entry" in keys_in_dic:
                    new_dic[flattened_key[:-1]] = obj
                else:
                    for current_key in obj:
                        flatten(obj[current_key], flattened_key + current_key + '|')
            elif type(obj) is list:
                i = 0
                for item in obj:
                    flatten(item, flattened_key + str(i) + '|')
                    i += 1
            else:
                new_dic[flattened_key[:-1]] = obj

        flatten(json_obj)

        return new_dic

    def design_json_table(self, flat_json_obj:dict):
        custom_ordered_dict = self._bring_to_top(flat_json_obj, "phase", self.custom_phase_order)
        custom_date_ordered_dict_list = self._sort_inner_activities(custom_ordered_dict)
        custom_ordered_phase_dict = self._group_by_sorted_phases(custom_date_ordered_dict_list)

        custom_phase_order = [item for item in list(custom_ordered_phase_dict.keys())]
        custom_entry_order = []
        for entries in [item["entries"] for item in list(custom_ordered_phase_dict.values())]:
            custom_entry_order += entries
        
        custom_ordered_overall_dict = [custom_ordered_dict[item] for item in custom_entry_order]
        df_table = pd.DataFrame(custom_ordered_overall_dict)
        df_table.fillna("N/A", inplace=True)

        return df_table, custom_ordered_overall_dict, custom_phase_order

    def _bring_to_top(self, unordered_dict_list:list, category:str, order_cons:list) -> dict:
        categorized_list = []
        custom_order = []
        normalized_category = category.lower().strip()

        normalized_dict_list = [
            {**item, normalized_category: item[normalized_category]} 
            for item in unordered_dict_list 
            if item.get(normalized_category) is not None
        ]

        for normalized_value in order_cons:
            for item in normalized_dict_list:
                if normalized_value.lower().strip() in item[normalized_category].lower().strip():
                    categorized_list.append(item)

        remaining_list = [
            item for item in unordered_dict_list
            if item not in categorized_list
        ]

        custom_ordered_dict = categorized_list + remaining_list

        for item in custom_ordered_dict:
            value = item[category]
            if value not in custom_order:
                custom_order.append(value)
        
        custom_ordered_dict = {item["entry"]:item for item in custom_ordered_dict}
        return custom_ordered_dict

    def _sort_inner_activities(self, json_obj:dict) -> list:
        ref_location = list(json_obj.values())[0]["area"]
        nested_loc_list = []
        same_loc_list = []

        for _, value in json_obj.items():
            if value["area"] != ref_location:
                nested_loc_list.append(same_loc_list)
                ref_location = value["area"]
                same_loc_list = [value]
            else:
                same_loc_list.append(value)

        nested_loc_list.append(same_loc_list)

        ordered_list = []
        for unordered_list in nested_loc_list:
            ordered_list += self._bubble_sort_entries_by_dates(unordered_list)

        return ordered_list

    def _bubble_sort_entries_by_dates(self, unsorted_list:list) -> list:
        n = len(unsorted_list)

        for i in range(n):
            for j in range(0, n-i-1):
                date_typed_start = datetime.strptime(unsorted_list[j]["start"], "%d-%b-%Y")
                date_typed_start_n1 = datetime.strptime(unsorted_list[j+1]["start"], "%d-%b-%Y")

                if date_typed_start > date_typed_start_n1:
                    unsorted_list[j], unsorted_list[j+1] = unsorted_list[j+1], unsorted_list[j]

                elif date_typed_start == date_typed_start_n1:
                    date_typed_end = datetime.strptime(unsorted_list[j]["finish"], "%d-%b-%Y")
                    date_typed_end_n1 = datetime.strptime(unsorted_list[j+1]["finish"], "%d-%b-%Y")

                    if date_typed_end > date_typed_end_n1:
                        unsorted_list[j], unsorted_list[j+1] = unsorted_list[j+1], unsorted_list[j]
        
        sorted_list = unsorted_list
        return sorted_list
    
    def _group_by_sorted_phases(self, json_obj:dict) -> dict:
        ref_phase = json_obj[0]["phase"]
        nested_phase_list = []
        same_phase_list = []

        for item in json_obj:
            if item["phase"] != ref_phase:
                nested_phase_list.append(same_phase_list)
                ref_phase = item["phase"]
                same_phase_list = [item]
            else:
                same_phase_list.append(item)

        nested_phase_list.append(same_phase_list)
        ordered_phase_dict = self._generate_phase_heirarchy(nested_phase_list, ["procurement", "milestone"])

        return ordered_phase_dict
    
    def _generate_phase_heirarchy(self, nested_phase_list:list, order_cons:list) -> dict:
        phase_dict = {}

        for unordered_list in nested_phase_list:
            start_dates = [item["start"] for item in unordered_list]
            finish_dates = [item["finish"] for item in unordered_list]
            earliest_date = self._bubble_sort_dates(start_dates)[0]
            latest_date = self._bubble_sort_dates(finish_dates)[-1]

            current_phase = unordered_list[0]["phase"]

            if current_phase not in phase_dict:
                latest_date_obj = datetime.strptime(latest_date, "%d-%b-%Y")
                earliest_date_obj = datetime.strptime(earliest_date, "%d-%b-%Y")
                midpoint_calc = earliest_date_obj + (latest_date_obj - earliest_date_obj) / 2

                phase_dict[current_phase] = {
                    "entries": [item["entry"] for item in unordered_list],
                    "start_list": start_dates,
                    "finish_list": finish_dates,
                    "earliest_date": earliest_date,
                    "latest_date": latest_date,
                    "midpoint_date": midpoint_calc.strftime("%d-%b-%Y"),
                }
            else:
                phase_dict[current_phase]["entries"].extend([item["entry"] for item in unordered_list])
                phase_dict[current_phase]["start_list"].extend(start_dates)
                phase_dict[current_phase]["finish_list"].extend(finish_dates)

                all_start_dates = phase_dict[current_phase]["start_list"]
                all_finish_dates = phase_dict[current_phase]["finish_list"]
                new_earliest_date = self._bubble_sort_dates(all_start_dates)[0]
                new_latest_date = self._bubble_sort_dates(all_finish_dates)[-1]
                latest_date_obj = datetime.strptime(new_latest_date, "%d-%b-%Y")
                earliest_date_obj = datetime.strptime(new_earliest_date, "%d-%b-%Y")
                midpoint_calc = earliest_date_obj + (latest_date_obj - earliest_date_obj) / 2

                phase_dict[current_phase]["earliest_date"] = new_earliest_date
                phase_dict[current_phase]["latest_date"] = new_latest_date
                phase_dict[current_phase]["midpoint_date"] = midpoint_calc.strftime("%d-%b-%Y")

        overall_dates_dict = self._calculate_overall_date(phase_dict)
        overall_dates_list = [{key: value["overall_date"]} for key, value in overall_dates_dict.items()]

        con_phases = []
        uncon_phases = []
        for item in overall_dates_list:
            skip = False

            for con in order_cons:
                if con in list(item.keys())[0].lower():
                    con_phases.append(item)
                    skip = True

            if skip:
                continue
            else:
                uncon_phases.append(item)

        ordered_overall_dates_list = self._bubble_sort_entries_by_overall_date(con_phases) + self._bubble_sort_entries_by_overall_date(uncon_phases)
        ordered_phase_dict = {
            list(item.keys())[0]: overall_dates_dict[list(item.keys())[0]] for item in ordered_overall_dates_list
        }

        return ordered_phase_dict

    def _bubble_sort_dates(self, unsorted_list:list) -> list:
        n = len(unsorted_list)

        for i in range(n):
            for j in range(n-i-1):
                value_j = unsorted_list[j]
                value_j1 = unsorted_list[j+1]

                try:
                    if isinstance(value_j, str) and isinstance(value_j1, str):
                        value_j = datetime.strptime(value_j, "%d-%b-%Y")
                        value_j1 = datetime.strptime(value_j1, "%d-%b-%Y")

                    elif isinstance(value_j, datetime) and isinstance(value_j1, datetime):
                        value_j = value_j
                        value_j1 = value_j1
                except Exception as e:
                    print(f"Error: {e}")
                else:
                    if value_j > value_j1:
                        unsorted_list[j], unsorted_list[j+1] = unsorted_list[j+1], unsorted_list[j]

        return unsorted_list

    def _bubble_sort_entries_by_overall_date(self, unsorted_list:list) -> list:
        n = len(unsorted_list)

        for i in range(n):
            for j in range(0, n-i-1):
                key_j = list(unsorted_list[j].keys())[0]
                key_j1 = list(unsorted_list[j + 1].keys())[0]

                date_j = datetime.strptime(unsorted_list[j][key_j], "%d-%b-%Y")
                date_j1 = datetime.strptime(unsorted_list[j + 1][key_j1], "%d-%b-%Y")

                if date_j > date_j1:
                    unsorted_list[j], unsorted_list[j + 1] = unsorted_list[j + 1], unsorted_list[j]

        return unsorted_list

    def _calculate_overall_date(self, phase_dict:dict) -> dict:
        for _, value in phase_dict.items():
            overall_date_delta = timedelta(0)

            current_start_list = value["start_list"]
            current_finish_list = value["finish_list"]
            current_midpoint_obj = datetime.strptime(value["midpoint_date"], "%d-%b-%Y")
            earliest_date_obj = datetime.strptime(value["earliest_date"], "%d-%b-%Y")
            latest_date_obj = datetime.strptime(value["latest_date"], "%d-%b-%Y")

            total_range_days = (latest_date_obj - earliest_date_obj).days

            # Validate total range
            if total_range_days <= 0:
                value["overall_date"] = current_midpoint_obj.strftime("%d-%b-%Y")
                continue

            for idx, start_date in enumerate(current_start_list):
                start_date_obj = datetime.strptime(start_date, "%d-%b-%Y")
                finish_date_obj = datetime.strptime(current_finish_list[idx], "%d-%b-%Y")

                avg_date = start_date_obj + (finish_date_obj - start_date_obj) / 2

                if avg_date < current_midpoint_obj:
                    weight = (current_midpoint_obj - avg_date).days / total_range_days
                    overall_date_delta -= timedelta(days=weight * total_range_days * 0.1)
                elif avg_date > current_midpoint_obj:
                    weight = (avg_date - current_midpoint_obj).days / total_range_days
                    overall_date_delta += timedelta(days=weight * total_range_days * 0.1)

            overall_date = current_midpoint_obj + overall_date_delta

            if overall_date < earliest_date_obj:
                overall_date = earliest_date_obj
            elif overall_date > latest_date_obj:
                overall_date = latest_date_obj

            value["overall_date"] = overall_date.strftime("%d-%b-%Y")

        return phase_dict

    def generate_wbs_cfa_style(self, df_table, categories_list:list, category:str):
        custom_entry_list = list(df_table["entry"])
        df_table["phase"] = pd.Categorical(df_table[category], categories=categories_list, ordered=True)
        df_table["entry"] = pd.Categorical(df_table["entry"], categories=custom_entry_list, ordered=True)

        proc_table = pd.pivot_table(
            df_table,
            index=self.project_table_index,
            values=self.project_table_values,
            aggfunc="first",
            observed=True
        )
        column_header_list = proc_table.columns.tolist()

        if "finish" in column_header_list and column_header_list[-1] != "finish":
            ordered_header_list = self._order_table_cols(column_header_list)
        else:
            ordered_header_list = column_header_list

        proc_table = proc_table[ordered_header_list]

        return proc_table

    def _order_table_cols(self, column_list:list) -> list:
        for idx, col in enumerate(column_list):
            if col == "finish":
                temp = column_list[-1]
                column_list[-1] = col
                column_list[idx] = temp
                break
        
        return column_list
    
    def determine_schedule_structure(self, custom_ordered_dict:list) -> str:
        for category in reversed(self.wbs_final_categories):
            has_valid_entry = any(item.get(category) for item in custom_ordered_dict)
            
            if has_valid_entry:
                return category

        return None


if __name__ == "__main__":
    project_details = DataFrameSetup.main(False)
