import os
import re
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Imported Helper - As Module
from utils.data_frame_setup import DataFrameSetup

# Imported Helper - As Package 
#from modules.utils.data_frame_setup import DataFrameSetup

class AnalyticsFramework:
    def __init__(self, input_json_path, input_json_basename):
        self.json_path = input_json_path
        self.json_basename = input_json_basename

        #Structures
        self.color_light_mode = {
            "font": dict(family="Rubik", size=14, color="#261F29"),
            "coloraxis_colorbar": dict(
                title="Activity Count",
                title_font_size=14,
                tickfont_size=12,
                title_font_color="#261F29",
                tickfont_color="#261F29",
            ),
            "plot_bgcolor": "#F9F9F9",
            "paper_bgcolor": "#F9F9F9",
            "axis": dict(
                showgrid=True,
                gridcolor="#DDDDDD",
                tickfont=dict(color="#261F29")
            ),
        }
        self.color_dark_mode = {
            "font": dict(family="Rubik", size=14, color="#FFFFFF"),
            "coloraxis_colorbar": dict(
                title="Activity Count",
                title_font_size=14,
                tickfont_size=12,
                title_font_color="#FFFFFF",
                tickfont_color="#FFFFFF",
            ),
            "plot_bgcolor": "#1F1F1F",
            "paper_bgcolor": "#121212",
            "axis": dict(
                showgrid=True,
                gridcolor="#333333",
                tickfont=dict(color="#FFFFFF"),
            ),
        }
        self.fig_color_modes = {
            "light": self.color_light_mode,
            "dark": self.color_dark_mode,
        }
    
    @staticmethod
    def main():
        project = AnalyticsFramework.generate_ins()
        project_details = DataFrameSetup.main(False)

        proc_table = project_details.get("proc_table")

        # KPI's - Lagging
        project.generate_lagging_indicators(proc_table)
    
    @staticmethod
    def generate_ins():
        input_json_file = input("Please enter the path to the Json file or directory: ")

        input_json_path, input_json_basename = AnalyticsFramework.file_verification(
            input_json_file, 'j', 'r')

        ins = AnalyticsFramework(input_json_path, input_json_basename)

        return ins
    
    @staticmethod
    def auto_genarate_ins():
        """ input_json_path, input_json_basename = AnalyticsFramework.file_verification(
            input_json_file, 'j', 'r')

        ins = AnalyticsFramework(input_json_path, input_json_basename)

        return ins """
        pass
    
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
        self._hardest_zones_heatmap(df_table)
        self._slowest_trade_column_chart(df_table)
        self._busiest_phases_donut(df_table)
        self._trades_contribution_to_phase_column_chart(df_table)
        self._trades_contribution_to_locations_column_chart(df_table)

    def _hardest_zones_heatmap(self, df_table, color_mode="light"):
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
                title="<b>Hardest Zones Heatmap</b><br><sup>Activity Count by Phase and Location</sup>",
                labels={"activity_count": "Activity Count", "location": "Location", "phase": "Phase"},
                color_continuous_scale="Plasma",
                text_auto=True,
                width=800,
                height=600,
            )

            fig_dict = self.fig_color_modes.get(color_mode)
            fig.update_layout(
                title_x=0.5,
                title_font_size=24,
                title_font_family=fig_dict["font"]["family"],
                xaxis_title="Location",
                yaxis_title="Phase",
                xaxis_title_font_size=16,
                yaxis_title_font_size=16,
                font=fig_dict["font"],
                margin=dict(l=50, r=50, t=100, b=50),
                coloraxis_colorbar=fig_dict["coloraxis_colorbar"],
                plot_bgcolor=fig_dict["plot_bgcolor"],
                paper_bgcolor=fig_dict["paper_bgcolor"],
                xaxis=fig_dict["axis"],
                yaxis=fig_dict["axis"],
            )

            output_file = f"hardest_zones_heatmap_{color_mode}.png"
            fig.write_image(output_file, scale=2)
            print(f"Heatmap saved as '{output_file}'")

        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def _slowest_trade_column_chart(self, df_table, color_mode="light"):
        df_table["start"] = pd.to_datetime(df_table["start"])
        df_table["finish"] = pd.to_datetime(df_table["finish"])
        df_table["duration"] = (df_table["finish"] - df_table["start"]).dt.days

        longest_trades = (
            df_table.groupby(["phase", "trade"], observed=True)
            .agg(total_duration=("duration", "sum"))
            .reset_index()
            .sort_values(by="total_duration", ascending=False)
        )

        longest_per_phase = longest_trades.groupby("phase", observed=True).head(3)

        try:
            fig = px.bar(
                longest_per_phase,
                x="phase",
                y="total_duration",
                color="trade",
                title="<b>Slowest Trade by Phase</b><br><sup>Top 3 Longest Trades per Phase</sup>",
                labels={"total_duration": "Total Duration (days)", "phase": "Phase"},
                barmode="stack",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )

            fig_dict = self.fig_color_modes.get(color_mode)
            fig.update_layout(
                title_x=0.5,
                title_font_size=24,
                title_font_family=fig_dict["font"]["family"],
                xaxis_title="Phase",
                yaxis_title="Total Duration (days)",
                xaxis_title_font_size=16,
                yaxis_title_font_size=16,
                font=fig_dict["font"],
                margin=dict(l=50, r=50, t=100, b=50),
                plot_bgcolor=fig_dict["plot_bgcolor"],
                paper_bgcolor=fig_dict["paper_bgcolor"],
                xaxis=fig_dict["axis"],
                yaxis=fig_dict["axis"],
                legend=dict(
                    title_text="Trade",
                    font=dict(size=12, color=fig_dict["font"]["color"])
                )
            )

            output_file = f"slowest_trade_column_chart_{color_mode}.png"
            fig.write_image(output_file, scale=2)
            print(f"Chart saved as '{output_file}'")

        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def _busiest_phases_donut(self, df_table, color_mode="light"):
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
                data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.3,
                    textinfo="label+percent",
                    insidetextorientation="radial",
                    marker=dict(colors=px.colors.qualitative.Plotly)
                )]
            )

            fig_dict = self.fig_color_modes.get(color_mode)
            fig.update_layout(
                title=dict(
                    text="<b>Busiest Phases</b><br><sup>Activity Count by Phase</sup>",
                    x=0.5,
                    font=dict(
                        size=24,
                        family=fig_dict["font"]["family"],
                        color=fig_dict["font"]["color"]
                    )
                ),
                font=fig_dict["font"],
                margin=dict(l=50, r=50, t=100, b=50),
                plot_bgcolor=fig_dict["plot_bgcolor"],
                paper_bgcolor=fig_dict["paper_bgcolor"],
                legend=dict(
                    title_text="Phase",
                    font=dict(size=12, color=fig_dict["font"]["color"])
                )
            )

            output_file = f"busiest_phases_donut_{color_mode}.png"
            fig.write_image(output_file, scale=2)
            print(f"Donut saved as '{output_file}'")

        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def _trades_contribution_to_phase_column_chart(self, df_table, color_mode="light"):
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
                title="<b>Trade Contributions to Phases</b><br><sup>Activity Count by Trade and Phase</sup>",
                labels={"phase": "Phase", "activity_count": "Activity Count"},
                text_auto=True,
                color_discrete_sequence=px.colors.qualitative.Plotly
            )

            fig_dict = self.fig_color_modes.get(color_mode)

            fig.update_layout(
                title_x=0.5,
                title_font_size=24,
                title_font_family=fig_dict["font"]["family"],
                xaxis_title="Phase",
                yaxis_title="Number of Activities",
                xaxis_title_font_size=16,
                yaxis_title_font_size=16,
                font=fig_dict["font"],
                margin=dict(l=50, r=50, t=100, b=50),
                plot_bgcolor=fig_dict["plot_bgcolor"],
                paper_bgcolor=fig_dict["paper_bgcolor"],
                xaxis=fig_dict["axis"],
                yaxis=fig_dict["axis"],
                legend=dict(
                    title_text="Trade",
                    font=dict(size=12, color=fig_dict["font"]["color"])
                ),
                barmode="stack"
            )

            output_file = f"trades_contributions_stacked_chart_{color_mode}.png"
            fig.write_image(output_file, scale=2)
            print(f"Chart saved as '{output_file}'")

        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def _trades_contribution_to_locations_column_chart(self, df_table, color_mode="light"):
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
                title="<b>Trade Contributions to Locations</b><br><sup>Activity Count by Trade and Location</sup>",
                labels={"location": "Location", "activity_count": "Activity Count"},
                text_auto=True,
                color_discrete_sequence=px.colors.qualitative.Plotly
            )

            fig_dict = self.fig_color_modes.get(color_mode)
            fig.update_layout(
                title_x=0.5,
                title_font_size=24,
                title_font_family=fig_dict["font"]["family"],
                xaxis_title="Locations",
                yaxis_title="Number of Activities",
                xaxis_title_font_size=16,
                yaxis_title_font_size=16,
                font=fig_dict["font"],
                margin=dict(l=50, r=50, t=100, b=50),
                plot_bgcolor=fig_dict["plot_bgcolor"],
                paper_bgcolor=fig_dict["paper_bgcolor"],
                xaxis=fig_dict["axis"],
                yaxis=fig_dict["axis"],
                legend=dict(
                    title_text="Trade",
                    font=dict(size=12, color=fig_dict["font"]["color"])
                ),
                barmode="stack",
            )

            output_file = f"trades_contributions_to_locations_stacked_chart_{color_mode}.png"
            fig.write_image(output_file, scale=2)
            print(f"Chart saved as '{output_file}'")

        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")


if __name__ == "__main__":
    AnalyticsFramework.main()
