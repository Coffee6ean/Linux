import os
import json
import pandas as pd
from openpyxl import load_workbook

class TypedScheduleProcessing():
    def __init__(self):
        self.json_path = "/home/coffee_6ean/Linux/CriticalFlowPath/results/json/cpm.json"
        self.typed_ordered_json = "/home/coffee_6ean/Linux/CriticalFlowPath/results/json/reordered_cpm.json"
        self.filled_excel_path = "/home/coffee_6ean/Linux/CriticalFlowPath/results/excel/filled_test_output.xlsx"
        self.column_categories = [
            "scope_of_work",
            "phase",
            "trade",
            "company",
            "location"
        ]
        self.trade_list_validation = [
            "Bricklayer",
            "Carpenter",
            "Cement Mason",
            "Drywall Finisher",
            "Electrician",
            "Elevator Constructor",
            "Glazier",
            "Insulation Worker",
            "Ironworker",
            "Laborer",
            "Millwright",
            "N/A",
            "Operating Engineer",
            "Painter",
            "Pipefitter",
            "Roofer",
            "Sheet Metal Worker",
            "Plumber"
        ]
        self.phase_list_validation = [
            "Civil",
            "Comissioning",
            "Elevator",
            "Exteriors/Skin",
            "Foundations",
            "Framing Structure",
            "Garage",
            "Interior Finishes",
            "Interior Rough Ins",
            "Landscaping Decks",
            "N/A",
            "Roof",
            "Site Prep",
            "Site Utilities",
            "Structure",
            "Transformer Vault"
        ]
        self.scope_of_work_list_validation = [
            "Construction",
            "Concrete Works", 
            "Demolition",  
            "Electrical",
            "Finishes",
            "Framing",
            "HVAC",  
            "Insulation",  
            "Landscaping",  
            "N/A",
            "Painting",  
            "Paving",  
            "Plumbing",
            "Roofing",  
            "Site Work",
            "Structural Steel"
        ]

    @staticmethod
    def main():
        phase_schedule = TypedScheduleProcessing()

        """ for category in phase_schedule.column_categories:
            categorized_json = phase_schedule.selected_json_category(category)
            phase_schedule.write_data_to_excel(categorized_json, f"{category.capitalize()} Typed - Schedule") """
        
        categorized_json = phase_schedule.selected_json_category(phase_schedule.column_categories[1])
        phase_schedule.write_data_to_excel(categorized_json, "Critical Flow - Schedule")

    def selected_json_category(self, category):
        selected_obj = {}

        with open(self.typed_ordered_json, 'r') as file:
            json_obj = json.load(file)

        for obj in json_obj["project_content"]:
            if obj["header"] == category:
                selected_obj = obj
        
        return selected_obj

    def write_data_to_excel(self, categorized_json, sheet_name):
        if not categorized_json:
            print("No data to write.")
            return

        flatten_data = []
        for category in categorized_json["filled"].keys():
            flatten_data.extend(categorized_json["filled"][category])

        try:
            flatten_activities = []
            
            for activity in flatten_data:
                activity_dic = {
                    "phase": activity.get("phase", ""),
                    "location": activity.get("location", ""),
                    "trade": activity.get("trade", ""),
                    "parent_id": activity["parent_id"],
                    "id": activity["id"],
                    "name": activity["name"],
                    "start": activity["start"],
                    "finish": activity["finish"],
                }
                flatten_activities.append(activity_dic)
            flatten_df = pd.DataFrame(flatten_activities)
            
            with pd.ExcelWriter(self.filled_excel_path, engine="openpyxl", mode='a', if_sheet_exists="replace") as writer:
                flatten_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=3)
            
            print(f"Data successfully written to {sheet_name} in {self.filled_excel_path}.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    TypedScheduleProcessing.main()
