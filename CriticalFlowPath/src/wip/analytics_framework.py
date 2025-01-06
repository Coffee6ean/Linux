import os
import re
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

class AnalyticsFramework:
    def __init__(self, input_json_path, input_json_basename):
        self.json_path = input_json_path
        self.json_basename = input_json_basename
    
    @staticmethod
    def main():
        project = AnalyticsFramework.generate_ins()
        table, custom_ordered_dict, custom_phase_order = project.setup_project()

        # KPI's - Lagging
        project.generate_lagging_indicators(table)
    
    @staticmethod
    def generate_ins():
        input_json_file = input("Please enter the path to the Json file or directory: ")

        input_json_path, input_json_basename = AnalyticsFramework.file_verification(
            input_json_file, 'j', 'r')

        ins = AnalyticsFramework(input_json_path, input_json_basename)

        return ins
    
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
    def file_verification(input_file_path, file_type, mode, input_json_title=None):
        if input_json_title and os.path.isdir(input_file_path):
            file_basename = f"processed_{AnalyticsFramework.normalize_entry(input_json_title)}.json"
            path, basename = AnalyticsFramework.handle_file(input_file_path, file_basename, file_type)
        else:
            if os.path.isdir(input_file_path):
                file_path, file_basename = AnalyticsFramework.handle_dir(input_file_path, mode)
                if mode != 'c':
                    path, basename = AnalyticsFramework.handle_file(file_path, file_basename, file_type)
                else:
                    path = file_path
                    basename = file_basename
            elif os.path.isfile(input_file_path):
                file_path = os.path.dirname(input_file_path)
                file_basename = os.path.basename(input_file_path)
                path, basename = AnalyticsFramework.handle_file(file_path, file_basename, file_type)

        return path, basename
    
    @staticmethod
    def handle_dir(input_path, mode):
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_path)
            selection = AnalyticsFramework.display_directory_files(dir_list)
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

        if (file_type == 'e' and AnalyticsFramework.is_xlsx(file)) or \
           (file_type == 'j' and AnalyticsFramework.is_json(file)):
            return os.path.dirname(file), os.path.basename(file)
        
        print("Error: Please verify that the directory and file exist and that the file is of type .xlsx or .json")
        return -1
    
    @staticmethod
    def normalize_entry(entry_str):
        remove_bewteen_parenthesis = re.sub('(?<=\()(.*?)(?=\))', '', entry_str)
        special_chars = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        remove_special_chars = re.sub(special_chars, '', remove_bewteen_parenthesis.lower())
        normalized_str = re.sub(' ', '_', remove_special_chars)

        return normalized_str
    
    def generate_lagging_indicators(self, df_table):
        self.hardest_zones_heatmap(df_table)
        self.slowest_trade_column_chart(df_table)
        self.busiest_phases_donut(df_table)
        self.trades_contribution_to_phase_column_chart(df_table)
        self.trades_contribution_to_locations_column_chart(df_table)

    def setup_project(self):
        flat_json_dict = self.read_json_dict()
        table, custom_ordered_dict, custom_phase_order = self.design_json_table(flat_json_dict)
        proc_table = self.generate_wbs_cfa_style(table, custom_phase_order, 'phase')

        print("Project set-up gone succesful")
        return proc_table, custom_ordered_dict, custom_phase_order

    def read_json_dict(self):
        j_file = os.path.join(self.json_path, self.json_basename)

        with open(j_file, 'r') as json_file:
            data = json.load(json_file)
        
        df = self.flatten_json(data["project_content"]["body"])
        df_values = list(df.values())

        return df_values

    def design_json_table(self, flat_json_dict):
        custom_ordered_dict = self.bring_to_top(flat_json_dict, "phase", ["procurement", "milestone"])
        custom_date_ordered_dict = self.sort_inner_activities(custom_ordered_dict)
        custom_ordered_phase_dict = self.group_by_sorted_phases(custom_date_ordered_dict)

        custom_phase_order = [item for item in list(custom_ordered_phase_dict.keys())]
        custom_entry_order = []
        for entries in [item["entries"] for item in list(custom_ordered_phase_dict.values())]:
            custom_entry_order += entries
        
        custom_ordered_overall_dict = [custom_ordered_dict[item] for item in custom_entry_order]
        df_table = pd.DataFrame(custom_ordered_overall_dict)
        return df_table, custom_ordered_overall_dict, custom_phase_order

    def bring_to_top(self, unordered_dict_list, category, order_cons):
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

    def sort_inner_activities(self, json_dict):
        ref_location = list(json_dict.values())[0]["location"]
        nested_loc_list = []
        same_loc_list = []

        for key, value in json_dict.items():
            if value["location"] != ref_location:
                nested_loc_list.append(same_loc_list)
                ref_location = value["location"]
                same_loc_list = [value]
            else:
                same_loc_list.append(value)

        nested_loc_list.append(same_loc_list)

        ordered_list = []
        for unordered_list in nested_loc_list:
            ordered_list += self.bubble_sort_entries_by_dates(unordered_list)

        return ordered_list

    def group_by_sorted_phases(self, json_dict:dict):
        ref_phase = json_dict[0]["phase"]
        nested_phase_list = []
        same_phase_list = []

        for item in json_dict:
            if item["phase"] != ref_phase:
                nested_phase_list.append(same_phase_list)
                ref_phase = item["phase"]
                same_phase_list = [item]
            else:
                same_phase_list.append(item)

        nested_phase_list.append(same_phase_list)
        ordered_phase_dict = self.generate_phase_heirarchy(nested_phase_list, ["procurement", "milestone"])

        return ordered_phase_dict

    def bubble_sort_entries_by_dates(self, unsorted_list:list):
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
    
    def bubble_sort_entries_by_overall_date(self, unsorted_list: list) -> list:
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
    
    def bubble_sort_dates(self, unsorted_list):
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

    def generate_phase_heirarchy(self, nested_phase_list:list, order_cons:list):
        phase_dict = {}
        for unordered_list in nested_phase_list:
            earliest_date = self.bubble_sort_dates([item["start"] for item in unordered_list])[0]
            latest_date = self.bubble_sort_dates([item["finish"] for item in unordered_list])[-1]

            current_phase = unordered_list[0]["phase"]
            if current_phase not in phase_dict:
                latest_date_obj = datetime.strptime(latest_date, "%d-%b-%Y")
                earliest_date_obj = datetime.strptime(earliest_date, "%d-%b-%Y")
                midpoint_calc = earliest_date_obj + (latest_date_obj - earliest_date_obj) / 2

                phase_dict[current_phase] = {
                    "entries": [item["entry"] for item in unordered_list],
                    "start_list": [item["start"] for item in unordered_list],
                    "finish_list": [item["finish"] for item in unordered_list],
                    "earliest_date": earliest_date,
                    "latest_date": latest_date,
                    "midpoint_date": midpoint_calc.strftime("%d-%b-%Y")
                }
        
        overall_dates_dict = self.calculate_overall_date(phase_dict)

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

        ordered_overall_dates_list = self.bubble_sort_entries_by_overall_date(con_phases) + self.bubble_sort_entries_by_overall_date(uncon_phases)
        ordered_phase_dict = {list(item.keys())[0]: overall_dates_dict[list(item.keys())[0]]  for item in ordered_overall_dates_list}

        return ordered_phase_dict

    def calculate_overall_date(self, phase_dict: dict):
        for key, value in phase_dict.items():
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

    def generate_wbs_cfa_style(self, df_table, categories_list, category):
        custom_entry_list = list(df_table["entry"])
        df_table["phase"] = pd.Categorical(df_table[category], categories=categories_list, ordered=True)
        df_table["entry"] = pd.Categorical(df_table["entry"], categories=custom_entry_list, ordered=True)

        proc_table = pd.pivot_table(
            df_table,
            index=["phase", "location", "entry", "activity_code"],
            values=["trade", "color", "activity_name", "start", "finish"],
            aggfunc="first",
            observed=True
        )
        column_header_list = proc_table.columns.tolist()

        if "finish" in column_header_list and column_header_list[-1] != "finish":
            ordered_header_list = self.order_table_cols(column_header_list)
        else:
            ordered_header_list = column_header_list

        proc_table = proc_table[ordered_header_list]

        return proc_table

    def order_table_cols(self, column_list):
        for idx, col in enumerate(column_list):
            if col == "finish":
                temp = column_list[-1]
                column_list[-1] = col
                column_list[idx] = temp
                break
        
        return column_list

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

    def hardest_zones_heatmap(self, df_table):
        heatmap_data = (
            df_table.groupby(["phase", "location"], observed=True)
            .size()
            .reset_index(name="activity_count")
        )
        proc_heatmap_data = heatmap_data.sort_values("activity_count")

        try:
            fig = px.density_heatmap(
                proc_heatmap_data,
                x="location",
                y="phase",
                z="activity_count",
                title="Hardest Zones Heatmap",
                labels={"activity_count": "Activity Count"},
                color_continuous_scale="Viridis",
                text_auto=True
            )

            fig.write_image("hardest_zones_heatmap.png")
            print("Heatmap saved as 'hardest_zones_heatmap.png'")
        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def slowest_trade_column_chart(self, df_table):
        df_table["start"] = pd.to_datetime(df_table["start"])
        df_table["finish"] = pd.to_datetime(df_table["finish"])

        df_table["duration"] = (df_table["finish"] - df_table["start"]).dt.days

        longest_trades = (
            df_table.groupby(["phase", "trade"], observed=True)
            .agg(total_duration=("duration", "sum"))
            .reset_index()
            .sort_values(by="total_duration", ascending=False)
        )

        longest_per_phase = (
            longest_trades.groupby("phase", observed=True)
            .head(3)
        )
        #print(longest_per_phase)

        """ trade_durations = (
            df_table.groupby(["phase", "trade"], observed=True)
            .agg(total_duration=("duration", "sum"))
            .reset_index()
        ) """
        try:
            fig = px.bar(
                longest_per_phase,
                x="phase",
                y="total_duration",
                color="trade",
                title="Slowest Trade by Phase",
                labels={"total_duration": "Total Duration (days)", "phase": "Phase"},
                barmode="stack"
            )

            fig.write_image("slowest_trade_column_chart.png")
            print("Chart saved as 'slowest_trade_column_chart.png'")
        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def busiest_phases_donut(self, df_table):
        donut_data = (
            df_table.groupby(["phase"], observed=True)
            .size()
            .reset_index(name="activity_count")
        )
        proc_donut_data = donut_data.sort_values("activity_count", ascending=False)

        labels = list(proc_donut_data["phase"])
        values = list(proc_donut_data["activity_count"])

        try:
            fig = go.Figure(
                data=[go.Pie(labels=labels, values=values, hole=.3)]
            )
            fig.update_layout(title=dict(text="Busiest Phases"))

            fig.write_image("busiest_phases_donut.png")
            print("Donut saved as 'busiest_phases_donut.png'")
        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def trades_contribution_to_phase_column_chart(self, df_table):
        column_chart = (
            df_table.groupby(["phase", "trade"], observed=True)
            .size()
            .reset_index(name="activity_count")
        )
        proc_column_chart = column_chart.sort_values("activity_count", ascending=False)

        try:
            fig = px.bar(
                proc_column_chart,
                x="phase",
                y="activity_count",
                color="trade",
                title="Trade Contributions to Phases",
                labels={"phase": "Phase", "activity_count": "Activity Count"},
                text_auto=True,
            )
            fig.update_layout(
                xaxis_title="Phase",
                yaxis_title="Number of Activities",
                legend_title="Trade",
                barmode="stack",
            )

            fig.write_image("trades_contributions_stacked_chart.png")
            print("Chart saved as 'trades_contributions_stacked_chart.png'")
        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def trades_contribution_to_locations_column_chart(self, df_table):
        column_chart = (
            df_table.groupby(["location", "trade"], observed=True)
            .size()
            .reset_index(name="activity_count")
        )
        proc_column_chart = column_chart.sort_values("activity_count", ascending=False)

        try:
            fig = px.bar(
                proc_column_chart,
                x="location",
                y="activity_count",
                color="trade",
                title="Trade Contributions to Locations",
                labels={"location": "Location", "activity_count": "Activity Count"},
                text_auto=True,
            )
            fig.update_layout(
                xaxis_title="Locations",
                yaxis_title="Number of Activities",
                legend_title="Trade",
                barmode="stack",
            )
            fig.write_image("trades_contributions_to_locations_stacked_chart.png")
            print("Chart saved as 'trades_contributions_to_locations_stacked_chart.png'")
        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")


if __name__ == "__main__":
    AnalyticsFramework.main()
