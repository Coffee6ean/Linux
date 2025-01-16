import os
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Imported Helper - As Module
from utils.data_frame_setup import DataFrameSetup

# Imported Helper - As Package 
#from modules.utils.data_frame_setup import DataFrameSetup

class AnalyticsFramework:
    def __init__(self, input_json_path, input_json_basename):
        self.json_path = input_json_path
        self.json_basename = input_json_basename

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
    def main():
        project = AnalyticsFramework.generate_ins()
        project_details = DataFrameSetup.main(False)

        proc_table = project_details.get("proc_table")
        lead_schedule_struct = project_details.get("lead_schedule_struct")

        # KPI's - Lagging
        project.generate_lagging_indicators(proc_table, lead_schedule_struct)
    
    @staticmethod
    def generate_ins():
        input_json_file = input("Please enter the path to the Json file or directory: ").strip()

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
    
    def generate_lagging_indicators(self, df_table, lead_schedule_struct:str):
        df_table_reset = df_table.reset_index()
        filtered_df = df_table_reset[~df_table_reset["phase"].isin(self.categories_not_needed)]

        self.hardest_zones_heatmap(filtered_df, lead_schedule_struct, "phase", "dark")
        self.hardest_zones_horizontal_bar(filtered_df, "phase", lead_schedule_struct, "dark")
        self.slowest_trade_column_chart(filtered_df, "phase", "trade", "dark")
        self.busiest_phases_donut(filtered_df, "phase", 0.05, "dark")
        self.contribution_column_chart(filtered_df, "phase", "trade", 0.075, "dark")
        self.contribution_column_chart(filtered_df, lead_schedule_struct, "trade", 0.075, "dark")
        self.lifeline_line_chart(filtered_df, "phase", "month", "dark")

    def hardest_zones_heatmap(self, df_table, category_x:str, category_y:str, 
                              color_mode:str="light") -> None:
        proc_heatmap_data = self._restructure_table_heatmap(
            df_table, 
            category_x,
            category_y, 
        )

        try:
            fig = px.density_heatmap(
                proc_heatmap_data,
                x=category_x,
                y=category_y,
                z="activity_count",
                title=f"<b>Hardest Zones Heatmap</b><br><sup>Activity Count by {category_x.capitalize()} and {category_y.capitalize()} (Top 10 Locations)</sup>",
                labels={
                    "activity_count": "Activity Count", 
                    category_x: category_x.capitalize(),
                    category_y: category_y.capitalize(),
                },
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
                xaxis_title=category_x.capitalize(),
                yaxis_title=category_y.capitalize(),
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

    def _restructure_table_heatmap(self, df_table, category_x:str, category_y:str):
        # Group by category_y and category_x, and calculate activity count
        heatmap_data = (
            df_table.groupby([category_y, category_x], observed=True)
            .size()
            .reset_index(name="activity_count")
        )

        # Calculate total activity count per category_x
        total_activity = heatmap_data.groupby(category_x, observed=True)["activity_count"].sum().reset_index()
        total_activity.columns = [category_x, "total_activity"]

        # Get the top 10 categories for category_x based on total activity count
        top_ten = total_activity.nlargest(10, "total_activity")[category_x]

        # Filter the heatmap data to include only the top 10 category_x values
        heatmap_data = heatmap_data[heatmap_data[category_x].isin(top_ten)]

        return heatmap_data
    
    def hardest_zones_horizontal_bar(self, df_table, category_x:str, category_y:str, 
                                    color_mode:str="light") -> None:
        # Restructure the data for the horizontal bar chart
        proc_bar_data = self._restructure_table_horizontal_bar(
            df_table, 
            category_x, 
            category_y
        )

        try:
            # Create the horizontal bar chart
            fig = px.bar(
                proc_bar_data,
                x="activity_count",
                y="hierarchy",  # Hierarchical sections (phase > lead)
                title=f"""<b>Hardest Zones Horizontal Bar Chart</b><br><sup>Activity Count by {category_x.capitalize()} and {category_y.capitalize()}</sup>
                """,
                labels={
                    "activity_count": "Activity Count", 
                    "hierarchy": "Hierarchy"
                },
                orientation="h",  # Horizontal bar chart
                width=1200,  # Increase width for better readability
                height=800,  # Increase height to accommodate hierarchical sections
                color_discrete_sequence=["#1f77b4"],  # Use a single color for all bars
            )

            # Apply color mode settings
            fig_dict = self.fig_color_modes.get(color_mode)
            fig.update_layout(
                title_x=0.5,
                title_font_size=24,
                title_font_family=fig_dict["font"]["family"],
                xaxis_title="Activity Count",
                yaxis_title="Hierarchy",
                xaxis_title_font_size=16,
                yaxis_title_font_size=16,
                font=fig_dict["font"],
                margin=dict(l=50, r=50, t=100, b=150),  # Increase bottom margin for legend
                plot_bgcolor=fig_dict["plot_bgcolor"],
                paper_bgcolor=fig_dict["paper_bgcolor"],
                xaxis=fig_dict["axis"],
                yaxis=fig_dict["axis"],
                showlegend=False,  # Hide legend since we're using a single color
            )

            # Save the chart as an image
            output_file = f"hardest_zones_horizontal_bar_{color_mode}.png"
            fig.write_image(output_file, scale=2)
            print(f"Horizontal bar chart saved as '{output_file}'")

        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def _restructure_table_horizontal_bar(self, df_table, category_x:str, category_y:str):
        # Convert categorical columns to strings (if necessary)
        df_table[category_x] = df_table[category_x].astype(str)
        df_table[category_y] = df_table[category_y].astype(str)

        # Group data hierarchically by phase > lead
        grouped_data = (
            df_table.groupby([category_x, category_y], observed=True)
            .size()
            .reset_index(name="activity_count")
        )

        # Create hierarchical labels (phase > lead)
        grouped_data["hierarchy"] = (
            grouped_data[category_x] + " > " + 
            grouped_data[category_y]
        )

        # Sort by activity_count in descending order and select the top 10
        grouped_data = grouped_data.sort_values("activity_count", ascending=False).head(10)

        return grouped_data

    def slowest_trade_column_chart(self, df_table, category_x:str, category_y:str, 
                                   color_mode:str="light") -> None:
        longest_per_phase = self._restructure_slowest_column_chart(df_table, category_x, category_y)

        try:
            fig = px.bar(
                longest_per_phase,
                x=category_x,
                y="total_duration",
                color=category_y,
                title="""
                <b>Slowest Trade by Phase</b><br><sup>Top 3 Longest Trades per Phase (Top 10 Phases)</sup>
                """,
                labels={
                    "total_duration": "Total Duration (days)",
                    category_x: category_x.capitalize()
                },
                barmode="stack",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )

            fig_dict = self.fig_color_modes.get(color_mode)
            fig.update_layout(
                title_x=0.5,
                title_font_size=24,
                title_font_family=fig_dict["font"]["family"],
                xaxis_title=category_x.capitalize(),
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
                    font=fig_dict["font"]
                )
            )

            output_file = f"slowest_trade_column_chart_{color_mode}.png"
            fig.write_image(output_file, scale=2)
            print(f"Chart saved as '{output_file}'")

        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def _restructure_slowest_column_chart(self, df_table, category_x:str, category_y:str):
        df_table["start"] = pd.to_datetime(df_table["start"])
        df_table["finish"] = pd.to_datetime(df_table["finish"])
        df_table["duration"] = (df_table["finish"] - df_table["start"]).dt.days

        longest_trades = (
            df_table.groupby([category_x, category_y], observed=True)
            .agg(total_duration=("duration", "sum"))
            .reset_index()
            .sort_values(by="total_duration", ascending=False)
        )

        top_phases = longest_trades[category_x].value_counts().nlargest(10).index
        longest_trades = longest_trades[longest_trades[category_x].isin(top_phases)]

        longest_per_phase = longest_trades.groupby(category_x, observed=True).head(3)
        
        return longest_per_phase

    def busiest_phases_donut(self, df_table, category:str, threshold:float=0.05, 
                             color_mode:str="light") -> None:
        labels, values = self._restructure_table_donut(df_table, category, threshold)

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
                    text=f"""
                    <b>Busiest: {category.capitalize()}</b><br><sup>Activity Count by Phase</sup>""",
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
                    title_text=category.capitalize(),
                    font=fig_dict["font"]
                )
            )

            output_file = f"busiest_phases_donut_{color_mode}.png"
            fig.write_image(output_file, scale=2)
            print(f"Donut saved as '{output_file}'")

        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def _restructure_table_donut(self, df_table, category:str, threshold:float):
        # Group and prepare data
        donut_data = (
            df_table.groupby([category], observed=True)
            .size()
            .reset_index(name="activity_count")
        )
        proc_donut_data = donut_data.sort_values("activity_count", ascending=False)

        # Calculate total activity count
        total_activity = proc_donut_data["activity_count"].sum()

        # Identify small categories (those below the threshold)
        proc_donut_data["proportion"] = proc_donut_data["activity_count"] / total_activity
        small_categories = proc_donut_data[proc_donut_data["proportion"] < threshold]
        large_categories = proc_donut_data[proc_donut_data["proportion"] >= threshold]

        # Group small categories into "Other"
        if not small_categories.empty:
            other_activity = small_categories["activity_count"].sum()
            other_row = pd.DataFrame({
                category: ["Other"],
                "activity_count": [other_activity],
                "proportion": [small_categories["proportion"].sum()]
            })
            proc_donut_data = pd.concat([large_categories, other_row], ignore_index=True)

        # Extract labels and values
        labels = list(proc_donut_data[category])
        values = list(proc_donut_data["activity_count"])

        return labels, values

    def contribution_column_chart(self, df_table, category_x:str, category_y:str, 
                                  threshold:float, color_mode:str="light") -> None:
        proc_column_chart = self._restructure_table_contribution_column_chart(
            df_table, 
            category_x, 
            category_y, 
            threshold
        )

        try:
            fig = px.bar(
                proc_column_chart,
                x=category_x,
                y="activity_count",
                color=category_y,
                title=f"""
                <b>{category_y.capitalize()} Contributions to {category_x.capitalize()} (Top 10 Trades)</b><br><sup>Activity Count by {category_y.capitalize()} and {category_x.capitalize()}</sup>
                """,
                labels={
                    category_x: category_x.capitalize(), 
                    "activity_count": "Activity Count"},
                text_auto=True,
                color_discrete_sequence=px.colors.qualitative.Plotly
            )

            fig_dict = self.fig_color_modes.get(color_mode)
            fig.update_layout(
                title_x=0.5,
                title_font_size=24,
                title_font_family=fig_dict["font"]["family"],
                xaxis_title=category_x.capitalize(),
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
                    title_text=category_y.capitalize(),
                    font=fig_dict["font"]
                ),
                barmode="stack"
            )

            output_file = f"{category_y}_contributions_to_{category_x}_stacked_chart_{color_mode}.png"
            fig.write_image(output_file, scale=2)
            print(f"Chart saved as '{output_file}'")

        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")

    def _restructure_table_contribution_column_chart(self, df_table, category_x:str, 
                                                category_y:str, threshold:float=0.05):
        # Group by category_x and category_y to calculate activity counts
        column_chart = (
            df_table.groupby([category_x, category_y], observed=True)
            .size()
            .reset_index(name="activity_count")
        )
        proc_column_chart = column_chart.sort_values("activity_count", ascending=False)

        # Calculate total activity per x-axis category
        total_activity_per_lead = proc_column_chart.groupby(
            category_x, 
            observed=True
        )["activity_count"].sum().reset_index()
        total_activity_per_lead.columns = [category_x, "total_activity"]

        # Merge total activity back into the main dataframe
        proc_column_chart = proc_column_chart.merge(total_activity_per_lead, on=category_x)

        # Calculate proportion of each y-axis category per x-axis category
        proc_column_chart["proportion"] = proc_column_chart["activity_count"] / proc_column_chart["total_activity"]

        # Identify small categories and group them into "Other"
        small_categories = proc_column_chart[proc_column_chart["proportion"] < threshold]
        large_categories = proc_column_chart[proc_column_chart["proportion"] >= threshold]

        # Create an "Other" category for each x-axis category
        other_data = small_categories.groupby(
            category_x,
            observed=True
        )["activity_count"].sum().reset_index()
        other_data[category_y] = "Other"
        other_data = other_data.merge(total_activity_per_lead, on=category_x)
        other_data["proportion"] = other_data["activity_count"] / other_data["total_activity"]

        # Combine large categories and "Other" data
        proc_column_chart = pd.concat([large_categories, other_data], ignore_index=True)

        # Sort x-axis categories by total activity and select the top 10
        top_10_x_categories = (
            total_activity_per_lead
            .sort_values("total_activity", ascending=False)
            .head(10)[category_x]
        )

        # Filter the data to include only the top 10 x-axis categories
        proc_column_chart = proc_column_chart[proc_column_chart[category_x].isin(top_10_x_categories)]

        return proc_column_chart

    def lifeline_line_chart(self, df_table, category:str, time_unit:str, 
                        color_mode:str="light") -> None:
        activity_counts = self._restructure_table_line_chart(
            df_table, 
            category, 
            time_unit
        )

        try:
            fig = px.line(
                activity_counts,
                x="time_period",
                y="activity_count",
                color=category,
                title=f"""
                <b>Busiest Time for {category.capitalize()}</b><br><sup>Activity Count Over Time (Top 10 {category.capitalize()}s)</sup>
                """,
                labels={
                    "activity_count": "Activity Count", 
                    "time_period": time_unit.capitalize(), 
                    category: category.capitalize()
                },
                line_shape="linear",  # Use "linear" or "spline" for smoother lines
                markers=True,  # Add markers to the line chart
            )

            fig_dict = self.fig_color_modes.get(color_mode)
            fig.update_layout(
                title_x=0.5,
                title_font_size=24,
                xaxis_title=time_unit.capitalize(),
                yaxis_title="Activity Count",
                xaxis_title_font_size=16,
                yaxis_title_font_size=16,
                font=fig_dict["font"],
                margin=dict(l=50, r=50, t=100, b=150),  # Increase bottom margin for legend
                plot_bgcolor=fig_dict["plot_bgcolor"],
                paper_bgcolor=fig_dict["paper_bgcolor"],
                xaxis=fig_dict["axis"],
                yaxis=fig_dict["axis"],
                legend=dict(
                    title_text=category.capitalize(),
                    font=dict(
                        family=fig_dict["font"]["family"],
                        size=12,  # Adjust legend font size if needed
                        color=fig_dict["font"]["color"]
                    ),
                    orientation="h",  # Horizontal legend
                    x=0.5,  # Center the legend horizontally
                    y=-0.2,  # Position the legend below the chart
                    xanchor="center",  # Anchor the legend at its center
                    yanchor="top"  # Anchor the legend at its top
                )
            )

            output_file = f"lifeline_line_chart_{category}_{time_unit}.png"
            fig.write_image(output_file, scale=2)
            print(f"Line chart saved as '{output_file}'")

        except Exception as e:
            print(f"An error occurred while creating the chart: {e}")
    
    def _restructure_table_line_chart(self, df_table, category:str, time_unit:str="month"):
        # Ensure the start and finish columns are datetime
        df_table["start"] = pd.to_datetime(df_table["start"])
        df_table["finish"] = pd.to_datetime(df_table["finish"])

        # Create a timeline for each activity
        timeline_data = []
        for _, row in df_table.iterrows():
            # Generate a date range for the activity
            date_range = pd.date_range(start=row["start"], end=row["finish"], freq="D")
            for date in date_range:
                timeline_data.append({
                    category: row[category],
                    "activity_code": row["activity_code"],  # Include activity_code
                    "date": date
                })

        # Convert the timeline data to a DataFrame
        timeline_df = pd.DataFrame(timeline_data)

        # Group by time unit and category
        if time_unit == "day":
            timeline_df["time_period"] = timeline_df["date"].dt.date
        elif time_unit == "week":
            timeline_df["time_period"] = timeline_df["date"].dt.to_period("W").dt.start_time
        elif time_unit == "month":
            timeline_df["time_period"] = timeline_df["date"].dt.to_period("M").dt.start_time
        else:
            raise ValueError("Invalid time_unit. Use 'day', 'week', or 'month'.")

        # Count the number of unique activities per time period and category
        activity_counts = (
            timeline_df.groupby(["time_period", category], observed=True)
            ["activity_code"].nunique()  # Count unique activity codes
            .reset_index(name="activity_count")
        )

        # Calculate total activity count per category
        total_activity = activity_counts.groupby(category)["activity_count"].sum().reset_index()
        total_activity.columns = [category, "total_activity"]

        # Merge total activity back into the main dataframe
        activity_counts = activity_counts.merge(total_activity, on=category)

        # Get the top 10 categories based on total activity count
        top_categories = total_activity.nlargest(10, "total_activity")[category]
        activity_counts = activity_counts[activity_counts[category].isin(top_categories)]

        return activity_counts


if __name__ == "__main__":
    AnalyticsFramework.main()
