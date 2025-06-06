import os
from datetime import datetime
from openpyxl.comments import Comment

class DataRelationship:
    def __init__(self, input_file_path, input_file_basename, 
                 input_file_extension, output_file_dir, project_data):
        self.input_path = input_file_path
        self.input_basename = input_file_basename
        self.input_extension = input_file_extension
        self.output_path = output_file_dir
        self.project_data = project_data

        #Structures
        self.json_categories = ["phase", "location", "area", "trade", "activity_code"]
        self.allowed_headers = {
            "activity_code": ["code", "task_code"],
            "activity_status": ["status", "task_status"],
            "hyperlinks": ["activity_code", "activity_name", "wbs_code"],
            "relationship_type": ["SS", "SF", "FS", "FF"]
        }

    @staticmethod
    def main(auto=True, input_file_path=None, input_file_basename=None, 
             input_file_extension=None, output_file_dir=None, project_data=None):
        if auto:
            project = DataRelationship.auto_generate_ins(
                input_file_path, 
                input_file_basename, 
                input_file_extension, 
                output_file_dir,
                project_data
            )
        else:
            project = DataRelationship.generate_ins()

        module_data = {
            "details": {
                "json": None,
                "df_rows": 0,
            },
            "logs": {
                "start": DataRelationship.return_valid_date(),
                "finish": None,
                "run-time": None,
            
           },
            "content": {}
        }

        if project:
            hyperlink_dict = project.create_hyperlinks(
                project.project_data["body"], 
                active_workbook=None, 
                active_worksheet=None
            )
            module_data["content"] = hyperlink_dict
        else:
            module_data["logs"]["status"] = {
                DataRelationship.__name__: "Error. Module's instance was not generated correctly"
            }

        return module_data
               
    @staticmethod
    def generate_ins():
        input_file = DataRelationship.return_valid_file(
            input("Please enter the path to the file or directory: ").strip()
        )
        output_file_dir = DataRelationship.return_valid_path(
            "Please enter the directory to save the new module results: "
        )

        ins = DataRelationship(
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
        ins = DataRelationship(
            input_file_path, 
            input_file_basename, 
            input_file_extension, 
            output_file_dir, 
            project_data
        )
        
        return ins
    
    @staticmethod
    def return_valid_file(input_file_dir:str) -> dict|int:        
        if not os.path.exists(input_file_dir):
            raise FileNotFoundError("Error: Given directory or file does not exist in the system.")

        if os.path.isdir(input_file_dir):
            file_dict = DataRelationship._handle_dir(input_file_dir)
        elif os.path.isfile(input_file_dir):
            file_dict = DataRelationship._handle_file(input_file_dir)

        return file_dict
    
    @staticmethod
    def _handle_dir(input_file_dir:str, mode:str="r") -> dict|int:
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_file_dir)
            selection = DataRelationship._display_directory_files(dir_list)
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

        if (input_file_extension in DataRelationship.allowed_extensions):
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

    def create_hyperlinks(self, custom_ordered_dict:dict, active_workbook, active_worksheet) -> dict:
        file = os.path.join(self.xlsx_path, self.xlsx_basename)

        hyperlink_entry_list = {key:value for key, value in custom_ordered_dict.items() 
                                if value.get("predecessor") is not None and len(value.get("predecessor")) > 1}
        hyperlink_dict = self._hyperlink_cells(active_worksheet, custom_ordered_dict, hyperlink_entry_list)

        """ active_workbook.save(filename=file)
        print("CFA Schedule successfully linked")
        active_workbook.close() """

        return hyperlink_dict

    def _hyperlink_cells(self, active_worksheet, custom_ordered_dict:dict, hyperlink_entry_list:list):
        ws = active_worksheet
        entry_dict = hyperlink_entry_list
        all_rltnshp_list = []
        embedded_list = []

        for _, value in entry_dict.items():
            embedded_list.append(self._verify_relationships(value))
        
        ovr_count = 1
        for relationship_list in embedded_list:
            for item in relationship_list:
                item["ovr_relationship_id"] = ovr_count
                ovr_count += 1

        for relationship_list in embedded_list:
            all_rltnshp_list += relationship_list

        link_dict = {item["ovr_relationship_id"]:item for item in all_rltnshp_list}
        ref_link_dict = self._generate_relationships(custom_ordered_dict, link_dict)

        # == WIP ==
        #nearest_links_dict = self._determine_nearest_links(ref_link_dict)

        #self._hyperlink_items(ws, ref_link_dict)
        return ref_link_dict

    def _verify_relationships(self, entry_dict:dict, relationship_count:int=1) -> list:
        rltshps = []
        current_pred_list = entry_dict.get("predecessor").split(',')
        current_succ_list = entry_dict.get("successor").split(',')
        current_type_list = entry_dict.get("relationship_type").split(',')
        
        if len(current_pred_list) == len(current_succ_list):
            for idx, pred in enumerate(current_pred_list):
                rltshps.append(
                    self._generate_relationship_dict(
                        entry_dict, 
                        relationship_count, 
                        pred, 
                        current_succ_list[idx], 
                        current_type_list[idx]
                    )
                )
                relationship_count += 1

        elif len(current_pred_list) > len(current_succ_list):
            print(f"Warning: Relationship defined in entry '{entry_dict['entry']}' is missing values.")
            available_links = len(current_succ_list)
            new_pred_list = current_pred_list[:available_links]

            for idx, pred in enumerate(new_pred_list):
                rltshps.append(
                    self._generate_relationship_dict(
                        entry_dict, 
                        relationship_count, 
                        pred, 
                        current_succ_list[idx], 
                        current_type_list[idx]
                    )
                )
                relationship_count += 1

        else:
            print(f"Warning: Relationship defined in entry '{entry_dict['entry']}' is missing values.")
            available_links = len(current_pred_list)
            new_succ_list = current_succ_list[:available_links]

            for idx, pred in enumerate(new_succ_list):
                rltshps.append(
                    self._generate_relationship_dict(
                        entry_dict, 
                        relationship_count, 
                        pred, 
                        current_succ_list[idx], 
                        current_type_list[idx]
                    )
                )
                relationship_count += 1

        return rltshps

    def _generate_relationship_dict(self, entry_dict:dict, count:int, pred:str, 
                                    succ:str, rel_type:str) -> dict:
        try:
            return {         
                "ref_entry": entry_dict["entry"],
                "relationship_id": count,
                "predecessor": pred.strip(),
                "successor": succ.strip(),
                "type": rel_type.strip()
            }
        except IndexError:
            print(f"Warning: Relationship type not defined in entry '{entry_dict['entry']}'. Falling back to default configuration.")
            return {         
                "ref_entry": entry_dict["entry"],
                "relationship_id": count,
                "predecessor": pred.strip(),
                "successor": succ.strip(),
                "type": "FS"
            }
        
    def _generate_relationships(self, custom_ordered_dict:dict, hyperlink_dict:dict) -> dict:
        for _, value in hyperlink_dict.items():
            current_pred = value.get("predecessor")
            current_succ = value.get("successor")
            
            ref_entry_pred, ref_pred_sequence = self._get_reference_entry(
                custom_ordered_dict, current_pred
            )
            ref_entry_succ, ref_succ_sequence = self._get_reference_entry(
                custom_ordered_dict, current_succ
            )

            if ref_entry_pred not in value:
                value["ref_entry_predecessor"] = ref_entry_pred
                value["predecessor_cell_sequence"] = ref_pred_sequence

            if ref_entry_succ not in value:
                value["ref_entry_successor"] = ref_entry_succ
                value["successor_cell_sequence"] = ref_succ_sequence

        return hyperlink_dict
    
    def _get_reference_entry(self, custom_ordered_dict:dict, entry_str:str, category:str="hyperlinks"):
        header = None
        ref_entry = None
        ref_cell_sequence = []

        for category in self.allowed_headers[category]:
            category_list = [value.get(category) for _, value in custom_ordered_dict.items()]

            if entry_str in category_list:
                header = category
                break

        for _, value in custom_ordered_dict.items():
            if value.get(header) == entry_str:
                ref_entry = value.get("entry")
                ref_cell_sequence = value.get("cell_sequence")

        return ref_entry, ref_cell_sequence

    def _determine_nearest_links(self, hyperlinks_dict:dict) -> dict:
        nearest_links = {}

        for _, value in hyperlinks_dict.items():
            current_entry = value.get("ref_entry")
            entry_pred = value.get("ref_entry_pred")
            entry_succ = value.get("ref_entry_succ")

            if current_entry not in nearest_links:
                nearest_links[current_entry] = {"nearest_link": None, "delta": float("inf")}

            if entry_pred and entry_succ:
                for linked_entry in [entry_pred, entry_succ]:
                    if linked_entry != current_entry:
                        delta = abs(current_entry - linked_entry)
                        if delta < nearest_links[current_entry]["delta"]:
                            nearest_links[current_entry]["nearest_link"] = linked_entry
                            nearest_links[current_entry]["delta"] = delta

        #print("Nearest Links:", nearest_links)
        return nearest_links

    def _hyperlink_items(self, active_worksheet, link_dict:dict, category:str="relationship_type") -> None:
        ws = active_worksheet

        for _, value in link_dict.items():
            curr_relationship_type = value.get("type")
            
            if curr_relationship_type in self.allowed_headers[category]:
                ref_entry_predecessor = value.get("ref_entry_predecessor")
                ref_entry_successor = value.get("ref_entry_successor")

                if curr_relationship_type == "SS":
                    if ref_entry_predecessor and ref_entry_successor:
                        start_cell_pred = value.get("predecessor_cell_sequence")[0]
                        start_cell_succ = value.get("successor_cell_sequence")[0]
                        self._add_hyperlink(ws, start_cell_pred, start_cell_succ)
                elif curr_relationship_type == "SF":
                    if ref_entry_predecessor and ref_entry_successor:
                        start_cell_pred = value.get("predecessor_cell_sequence")[0]
                        start_cell_succ = value.get("successor_cell_sequence")[-1]
                        self._add_hyperlink(ws, start_cell_pred, start_cell_succ)
                elif curr_relationship_type == "FS":
                    if ref_entry_predecessor and ref_entry_successor:
                        start_cell_pred = value.get("predecessor_cell_sequence")[-1]
                        start_cell_succ = value.get("successor_cell_sequence")[0]
                        self._add_hyperlink(ws, start_cell_pred, start_cell_succ)
                else:
                    if ref_entry_predecessor and ref_entry_successor:
                        start_cell_pred = value.get("predecessor_cell_sequence")[-1]
                        start_cell_succ = value.get("successor_cell_sequence")[-1]
                        self._add_hyperlink(ws, start_cell_pred, start_cell_succ)
        
    def _add_hyperlink(self, active_worksheet, predecessor_cell:str, successor_cell:str) -> None:
        ws = active_worksheet

        pred_cell = ws[predecessor_cell]
        succ_cell = ws[successor_cell]
        pred_comment = pred_cell.comment
        succ_comment = succ_cell.comment

        wb_name = self.xlsx_basename
        ws_title = ws.title

        succ_hprl_title = f"Link to {successor_cell}"
        succ_hyperlink_msg = f'=HYPERLINK("[{wb_name}]\'{ws_title}\'!{successor_cell}", "{succ_hprl_title}")'
        
        pred_hprl_title = f"Link to {predecessor_cell}"
        pred_hyperlink_msg = f'=HYPERLINK("[{wb_name}]\'{ws_title}\'!{predecessor_cell}", "{pred_hprl_title}")'

        if pred_comment:
            if "=== Successors ===" not in pred_comment.text:
                pred_comment.text += f"\n=== Successors ===\n"
            pred_comment.text += f"{succ_hyperlink_msg}\n"
        else:
            pred_cell.comment = Comment(f"=== Successors ===\n{succ_hyperlink_msg}\n", "AMP")

        if succ_comment:
            if "=== Predecessors ===" not in succ_comment.text:
                succ_comment.text += f"\n=== Predecessors ===\n"
            succ_comment.text += f"{pred_hyperlink_msg}\n"
        else:
            succ_cell.comment = Comment(f"=== Predecessors ===\n{pred_hyperlink_msg}\n", "AMP")


if __name__ == "__main__":
    DataRelationship.main(False)
