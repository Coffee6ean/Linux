import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Imported Helper - As Module
import setup

import sys
sys.path.append("../")
from CriticalFlowPath.keys.secrets import RSLTS_DIR

class AnalyticsFramework:
    def __init__(self, input_file_path, input_file_basename, input_file_extension, 
                 output_file_dir, project_table, project_lead_struct):
        self.input_path = input_file_path
        self.input_basename = input_file_basename
        self.input_extension = input_file_extension
        self.output_dir = output_file_dir
        self.table = project_table
        self.lead_struct = project_lead_struct

        #Structures
        self.categories_not_needed = ["procurement", "milestones"]
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
    def main(auto=True, input_file_path=None, input_file_basename=None, input_file_extension=None, 
             output_file_dir=None, project_table=None, project_lead_struct=None):
        if auto:
            project = AnalyticsFramework.auto_genarate_ins(
                input_file_path, 
                input_file_basename, 
                input_file_extension, 
                output_file_dir, 
                project_table,
                project_lead_struct
            )
        else:
            project = AnalyticsFramework.generate_ins()

        if project:
            project.generate_indicators(project.table, project.lead_struct)
    
    @staticmethod
    def generate_ins():
        AnalyticsFramework.ynq_user_interaction(
            "Run Module as stand-alone? "
        )

        setup_cls = setup.Setup.main()

        ins = AnalyticsFramework(
            setup_cls.obj["input_file"].get("path"), 
            setup_cls.obj["input_file"].get("basename"),
            setup_cls.obj["input_file"].get("extension"),
            RSLTS_DIR,
            setup_cls.obj["project"]["modules"]["MODULE_2"]["content"].get("table"),
            setup_cls.obj["project"]["modules"]["MODULE_2"]["content"].get("lead_schedule_struct"),
        )

        return ins
    
    @staticmethod
    def auto_genarate_ins(input_file_path, input_file_basename, input_file_extension, 
                          output_file_dir, project_table, project_lead_struct):
        ins = AnalyticsFramework(
            input_file_path,
            input_file_basename,
            input_file_extension,
            output_file_dir,
            project_table,
            project_lead_struct
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
    
    def generate_indicators(self, df_table, lead_schedule_struct:str):
        df_table_reset = df_table.reset_index()
        filtered_df = df_table_reset[~df_table_reset["phase"].isin(self.categories_not_needed)]

        self.generate_gantt_chart(filtered_df, "dark")
        #self.hardest_zones_heatmap(filtered_df, lead_schedule_struct, "phase", "dark")

    def generate_gantt_chart(self, df_table, color_mode:str) -> None:
        # Restructure data for Gantt chart
        proc_gantt_data = self._restructure_table_gantt(df_table)

        try:
            # Create Gantt chart for past schedule (muted colors)
            fig = px.timeline(
                proc_gantt_data,
                x_start="Past Start",
                x_end="Past Finish",
                y="Task",
                color="Phase",
                color_discrete_sequence=["lightgray", "lightblue"],  # Muted colors for past schedule
                title="<b>Schedule Comparison: Past vs. Current</b><br><sup>Top 10 Modified Tasks by Phase</sup>",
            )

            # Add current schedule bars (intense colors)
            fig.add_trace(
                px.timeline(
                    proc_gantt_data,
                    x_start="Current Start",
                    x_end="Current Finish",
                    y="Task",
                    color="Phase",
                    color_discrete_sequence=["orange", "blue"],  # Intense colors for current schedule
                ).data[0]
            )

            # Update layout with color mode settings
            fig_dict = self.fig_color_modes.get(color_mode)
            fig.update_layout(
                title_x=0.5,
                title_font_size=24,
                title_font_family=fig_dict["font"]["family"],
                xaxis_title="Date",
                yaxis_title="Task",
                xaxis_title_font_size=16,
                yaxis_title_font_size=16,
                font=fig_dict["font"],
                margin=dict(l=50, r=50, t=100, b=50),
                plot_bgcolor=fig_dict["plot_bgcolor"],
                paper_bgcolor=fig_dict["paper_bgcolor"],
                xaxis=fig_dict["axis"],
                yaxis=fig_dict["axis"],
            )

            # Add annotations for significant changes
            for index, row in proc_gantt_data.iterrows():
                if abs(row["Time Difference"]) > 0:  # Highlight tasks with changes
                    fig.add_annotation(
                        x=row["Current Start"],
                        y=row["Task"],
                        text=f"Shift: {row['Time Shift']} days",
                        showarrow=True,
                        arrowhead=1,
                        ax=0,
                        ay=-40,
                        bgcolor="red",
                        opacity=0.8,
                    )

            # Save the chart
            output_path = self.output_dir
            output_basename = f"gantt_chart_{color_mode}.png"
            output_file = os.path.join(output_path, output_basename)
            fig.write_image(output_file, scale=2)
            print(f"Gantt chart saved as '{output_file}'")

        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def _restructure_table_gantt(self, df_table):
        # Ensure required columns are present
        required_columns = [
            "Task", "Phase", "Past Start", "Past Finish", 
            "Current Start", "Current Finish", "Time Difference", "Time Shift"
        ]
        if not all(col in df_table.columns for col in required_columns):
            raise ValueError(f"Input DataFrame must contain the following columns: {required_columns}")

        # Sort by Time Difference to get the top 10 modified tasks
        top_ten_tasks = (
            df_table.sort_values(by="Time Difference", key=abs, ascending=False)
            .head(10)
        )

        return top_ten_tasks

if __name__ == "__main__":
    AnalyticsFramework.main()
