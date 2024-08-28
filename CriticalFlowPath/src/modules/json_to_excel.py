import os
import json
import pandas as pd
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell

# Global variables
output_file_name = None
output_folder = None
output_file_path = None
list_validation = [
    'Carpenter',
    'Electrician',
    'Plumber',
    'Ironworker',
    'Sheet Metal Worker',
    'Pipefitter',
    'Laborer',
    'N/A',
    'Operating Engineer',
    'Bricklayer',
    'Cement Mason',
    'Roofer',
    'Glazier',
    'Painter',
    'Drywall Finisher',
    'Insulation Worker',
    'Elevator Constructor',
    'Millwright'
]

class JsonToExcel(): 
    """
    A class for converting JSON data to an Excel file.
    """
    def __init__(self):
        pass

    @staticmethod
    def main():
        json_obj_instance = JsonToExcel()  # Create an instance of the JsonObj class
        wb, ws = json_obj_instance.create_workbook()  # Call the method to create the workbook
    
        if wb and ws:
            json_obj_instance.write_data_to_excel(output_file_path)  # Write JSON data to Excel
            print(f"Workbook created and saved at: {output_file_path}")

    def retrieve_json_file(self):
        """
        Retrieves the JSON data. It can accept a folder origin or the file path completely.

        Returns:
            list: A list containing the JSON data.

        Library: json
        """
        json_input_path = input("Please enter the path to the JSON file or directory: ")

        json_data = []
        if os.path.isfile(json_input_path) and json_input_path.endswith('.json'):
            print(f"Reading JSON file: {json_input_path}")
            with open(json_input_path, 'r') as f:
                json_data.append(json.load(f))
        elif os.path.exists(json_input_path):
            print(f"Looking for JSON files in: {json_input_path}")
            for json_input_file in os.listdir(json_input_path):
                if json_input_file.endswith("json"):
                    json_file_path = os.path.join(json_input_path, json_input_file)
                    with open(json_file_path, 'r') as f:
                        json_data.append(json.load(f))
            if not json_data:
                print('Error. Folder has no current JSON files')
        else:
            print('Error. Path not found in system')
        return json_data

    def create_workbook(self):
        """
        Creates a new Excel workbook and prompts the user for the output folder.

        Returns:
            tuple: The created workbook and worksheet objects.
            (Workbook, Worksheet)

        Library: openpyxl
        """
        global output_folder, output_file_path  # Declare global variables

        # Prompt the user for the output folder
        output_folder = input("Please enter the folder path to save the Excel file: ")

        # Check if the specified folder exists
        if not os.path.exists(output_folder):
            print("Error: The specified folder does not exist.")
            return None, None

        # If folder does exist, create new Workbook & Worksheet from openpyxl
        output_file = input("Please input file name: ")
        output_file_path = os.path.join(output_folder, f"{output_file}.xlsx")

        # Create a new workbook and select the active worksheet
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Project Content"  # Set a title for the worksheet

        return workbook, worksheet  # Return the workbook and worksheet for further use

    def write_data_to_excel(self, excel_file):
        """
        Writes the JSON data to an Excel file.

        Args:
            excel_file (str): The path to the Excel file where the data will be written.

        Library: pandas
        """
        # Retrieve JSON data
        extracted_json_data = self.retrieve_json_file()

        if extracted_json_data:
            # Assuming we only need the first JSON object
            data = extracted_json_data[0]  # If there are multiple JSON objects, handle accordingly

            # Prepare to write to Excel
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                # Write metadata as a title section
                metadata = data['project_metadata']
                metadata_df = pd.DataFrame(metadata.items(), columns=['Field', 'Value'])
                metadata_df.to_excel(writer, sheet_name='Metadata', index=False, startrow=1)

                # Extract header and body
                body = data['project_content']['body']

                # Prepare to flatten the body with activities
                flattened_data = []

                for entry in body:
                    # Add the parent activity row
                    parent_data = {
                        "parent_id": "N/A",  # Assuming no parent for top-level activities
                        'id': entry['id'],
                        'name': entry['name'],
                        'duration': entry['duration'],
                        'start': entry['start'],
                        'finish': entry['finish'],
                        'total_float': entry['total_float'],
                        "scope_of_work": entry.get('scope_of_work', ''),
                        "phase": entry.get('phase', ''),
                        "trade": entry.get('trade', ''),
                        "company": entry.get('company', ''),
                    }
                    flattened_data.append(parent_data)

                    # If there are activities, flatten them
                    if entry['activities']:
                        for activity in entry['activities']:
                            # Add child activity row
                            child_data = {
                                "parent_id": entry['id'],  # Set parent_id to the current entry's id
                                'id': activity['id'],
                                'name': activity['name'],
                                'duration': activity['duration'],
                                'start': activity['start'],
                                'finish': activity['finish'],
                                'total_float': activity['total_float'],
                                "scope_of_work": activity.get('scope_of_work', ''),
                                "phase": activity.get('phase', ''),
                                "trade": activity.get('trade', ''),
                                "company": activity.get('company', ''),
                            }
                            flattened_data.append(child_data)  # Append child data after the parent

                # Convert flattened data to DataFrame
                flattened_df = pd.DataFrame(flattened_data)

                # Write flattened body to a new sheet
                flattened_df.to_excel(writer, sheet_name='Project Content', index=False, startrow=2)

            print(f"Successfully converted JSON to Excel and saved to {excel_file}")
        else:
            print("Error: No data to convert.")


if __name__ == "__main__":
    json_obj_instance = JsonToExcel()  # Create an instance of the JsonObj class
    wb, ws = json_obj_instance.create_workbook()  # Call the method to create the workbook

    if wb and ws:
        json_obj_instance.write_data_to_excel(output_file_path)  # Write JSON data to Excel
        print(f"Workbook created and saved at: {output_file_path}")
