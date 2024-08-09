import os
import json
import pandas as pd

class JsonObj: 
    """
    A class for converting JSON data to an Excel file.
    """
    def __init__(self):
        pass

    def retrieve_json_file(self):
        """
        Retrieves the JSON data from the 'results' folder.

        Returns:
            list: A list containing the JSON data.
        """
        json_input_path = os.path.join(os.getcwd(), 'results')
        if os.path.exists(json_input_path):
            print(f"Looking for JSON files in: {json_input_path}")
            json_data = []
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

    def json_results_to_data_frame(self):
        """
        Converts the JSON data to an Excel file.
        """
        # Prompt the user for the output folder
        output_folder = input("Please enter the folder path to save the Excel file: ")
        
        # Check if the specified folder exists
        if not os.path.exists(output_folder):
            print("Error: The specified folder does not exist.")
            return

        # Retrieve JSON data
        json_data = self.retrieve_json_file()
        
        if json_data:
            # Assuming we only need the first JSON object
            data = json_data[0]  # If there are multiple JSON objects, handle accordingly

            # Prepare to write to Excel
            output_excel_file = os.path.join(output_folder, 'output.xlsx')
            with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
                # Write metadata as a title section
                metadata = data['project_metadata']
                metadata_df = pd.DataFrame(metadata.items(), columns=['Field', 'Value'])
                metadata_df.to_excel(writer, sheet_name='Metadata', index=False)

                # Extract header and body
                header = data['project_content']['header']
                body = data['project_content']['body']

                # Prepare to flatten the body with activities
                flattened_data = []

                for entry in body:
                    # Add the parent activity row
                    parent_data = {
                        'id': entry['id'],
                        'name': entry['name'],
                        'duration': entry['duration'],
                        'start': entry['start'],
                        'finish': entry['finish'],
                        'total_float': entry['total_float'],
                        'activity_id': None,
                        'activity_name': None,
                        'activity_duration': None,
                        'activity_start': None,
                        'activity_finish': None,
                        'activity_total_float': None
                    }
                    flattened_data.append(parent_data)

                    # If there are activities, flatten them
                    if entry['activities']:
                        for activity in entry['activities']:
                            # Add child activity row
                            child_data = {
                                'id': None,  # Parent ID is not needed here
                                'name': None,  # Parent name is not needed here
                                'duration': None,  # Parent duration is not needed here
                                'start': None,  # Parent start is not needed here
                                'finish': None,  # Parent finish is not needed here
                                'total_float': None,  # Parent total_float is not needed here
                                'activity_id': activity['id'],
                                'activity_name': activity['name'],
                                'activity_duration': activity['duration'],
                                'activity_start': activity['start'],
                                'activity_finish': activity['finish'],
                                'activity_total_float': activity['total_float']
                            }
                            flattened_data.append(child_data)

                # Convert flattened data to DataFrame
                flattened_df = pd.DataFrame(flattened_data)

                # Write flattened body to a new sheet
                flattened_df.to_excel(writer, sheet_name='Project Content', index=False)

            print(f"Successfully converted JSON to Excel and saved to {output_excel_file}")
        else:
            print("Error: No data to convert.")

# Example usage
if __name__ == "__main__":
    json_obj_instance = JsonObj()  # Create an instance of the JsonObj class
    json_obj_instance.json_results_to_data_frame()  # Call the method to convert JSON to Excel
