import json
import os
from datetime import datetime

class JsonPostProcessing:
    def __init__(self, json_obj):
        self.json_obj = json_obj
        self.reordered_json_list = []

    @staticmethod
    def main():
        json_file_input = input('Please enter the JSON file path to read: ')

        # Open and read the JSON file
        try:
            with open(json_file_input, mode='r') as json_file:
                json_obj = json.load(json_file)  # Load JSON data
                json_post_processing = JsonPostProcessing(json_obj['project_content']['body'])
                #json_post_processing.reorder_json(json_obj['project_content']['body'], None)  # Start the reordering process
                json_post_processing.test(json_obj['project_content']['body'], None)  # Start the reordering process

                # Output the reordered JSON
                output_file = os.path.join('/home/coffee_6ean/Linux/CriticalFlowPath/results/json', 'processed_cpm.json')
                with open(output_file, mode='w') as file:
                    json.dump(json_post_processing.reordered_json_list, file, indent=4)
                print("Reordered JSON saved successfully.")

        except FileNotFoundError:
            print("Error: The specified file does not exist.")
        except json.JSONDecodeError:
            print("Error: The file is not a valid JSON file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def pretty_print(json_obj):
        print(json.dumps(json_obj, indent=4))
    
    @staticmethod
    def parse_date(date_str):
        return datetime.strptime(date_str, "%d-%b-%y")

    def test(self, json_obj, first_parent=None):
        if isinstance(json_obj, list) and first_parent == None:
            for entry in json_obj:
                self.reordered_json_list.append(entry)
            first_parent = self.reordered_json_list[0]
            self.test(self.reordered_json_list, first_parent)
        else:
            #print(self.reordered_json_list)
            #print("Detected parent:", first_parent)
            for entry in self.reordered_json_list[1:]:
                self.test_sup_3(first_parent, entry)

    def test_sup(self, possible_parent, child, last_accepted_parent=None):
        if child != possible_parent:
            if 'activities' in possible_parent:
                dynamic_list = possible_parent['activities']

                # Check if the child falls within the parent's date range
                if (JsonPostProcessing.parse_date(possible_parent['start']) <= JsonPostProcessing.parse_date(child['start']) and
                    JsonPostProcessing.parse_date(possible_parent['finish']) >= JsonPostProcessing.parse_date(child['finish'])):

                    # Only process if the child has not been appended yet
                    if child not in dynamic_list:
                        if len(dynamic_list) > 0:
                            for activity in dynamic_list:
                                #print('New possible parent:', json.dumps(activity, indent=4))
                                #print('Child to fit:', json.dumps(child, indent=4))
                                #print('Last accepted parent:', json.dumps(possible_parent, indent=4))
                                self.test_sup(activity, child, possible_parent)
                        else:
                            dynamic_list.append(child)
                else:
                    # Ensure last_accepted_parent is valid and not None
                    if last_accepted_parent and child not in last_accepted_parent['activities']:
                        last_accepted_parent['activities'].append(child)
            else:
                # Ensure last_accepted_parent is valid and not None
                if last_accepted_parent and last_accepted_parent['activities'] and last_accepted_parent['activities'][-1] == possible_parent:
                    if child not in last_accepted_parent['activities']:
                        last_accepted_parent['activities'].append(child)
    
    #WIP
    def test_sup_2(self, possible_parent, child, parent_stack=[]):
        # This is to ensure that we do not fall in a circular reference
        # Since last activity has been added to parent_stack we now move forward with the rest of the entries
        if child not in parent_stack and child not in possible_parent['activities']:
            # This means that current activity being evaluated is of type 'child'
            if 'activities' in possible_parent:
                dynamic_list = possible_parent['activities']

                # Check if the child falls within the parent's date range
                if (JsonPostProcessing.parse_date(possible_parent['start']) <= JsonPostProcessing.parse_date(child['start']) and
                    JsonPostProcessing.parse_date(possible_parent['finish']) >= JsonPostProcessing.parse_date(child['finish'])):
                    
                    # This means that current activity being evaluated is of type 'parent' &
                    # the current child did fit into the parent's date range
                    parent_stack.append(possible_parent)

                    # Only process if the child has not been appended yet
                    if child not in dynamic_list:
                        if len(dynamic_list) > 0:
                            for activity in dynamic_list:
                                self.test_sup(activity, child, parent_stack)
                        else:
                            dynamic_list.append(child)
                            # Child has been graduated to a new 'possible_parent' for other future entries. Repeat cycle
                            parent_stack.append(child)
                else:
                    if possible_parent == dynamic_list[-1]:
                        # Extract last valid parent
                        last_accepted_parent = parent_stack.pop()
                        # Add current child to last valid parent
                        last_accepted_parent['activities'].append(child)
                        # Child has been graduated to a new 'possible_parent' for other future entries. Repeat cycle
                        parent_stack.append(child)
            else:
                # Ensure that we go through all the activities before appending the child
                # This is if we do not find a parent for the child throughout all options then we append
                #   to last valid parent
                if possible_parent == dynamic_list[-1]:
                    # Extract last valid parent
                    last_accepted_parent = parent_stack.pop()
                    # Add current child to last valid parent
                    last_accepted_parent['activities'].append(child)
                    # Child has been graduated to a new 'possible_parent' for other future entries. Repeat cycle
                    parent_stack.append(child)
    
    """ def test_sup_3(self, possible_parent, child, parent_stack=[]):
        if child not in parent_stack and child not in possible_parent['activities']:
            # This means that the current activity being evaluated is of type 'child'
            if 'activities' in possible_parent:
                dynamic_list = possible_parent['activities']

                # Check if the child falls within the parent's date range
                if (JsonPostProcessing.parse_date(possible_parent['start']) <= JsonPostProcessing.parse_date(child['start']) and
                    JsonPostProcessing.parse_date(possible_parent['finish']) >= JsonPostProcessing.parse_date(child['finish'])):
                    
                    # The current activity is of type 'parent' and the current child fits into the parent's date range
                    parent_stack.append(possible_parent)

                    # Only process if the child has not been appended yet
                    if child not in dynamic_list:
                        if len(dynamic_list) > 0:
                            for activity in dynamic_list:
                                # Recursively check each nested activity
                                self.test_sup_2(activity, child, parent_stack)
                                # Break after the first valid parent is found
                                if child in activity['activities']:
                                    break
                        else:
                            dynamic_list.append(child)  # Append child if no nested activities
                            parent_stack.append(child)  # Child has been graduated to a new 'possible_parent'
                else:
                    # If the child does not fit under the possible parent, append to last valid parent
                    if parent_stack:
                        last_accepted_parent = parent_stack[-1]  # Get the last valid parent
                        last_accepted_parent['activities'].append(child)  # Append child to last valid parent
                        parent_stack.append(child)  # Child has been graduated to a new 'possible_parent'
            else:
                # If there are no activities in the possible parent, append the child to the last valid parent
                if parent_stack:
                    last_accepted_parent = parent_stack[-1]  # Get the last valid parent
                    last_accepted_parent['activities'].append(child)  # Append child to last valid parent
                    parent_stack.append(child)  # Child has been graduated to a new 'possible_parent' """

if __name__ == "__main__":
    JsonPostProcessing.main()