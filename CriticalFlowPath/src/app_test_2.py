import os
import re
from datetime import datetime
import modules as mdls

class App:

    def __init__(self) -> None:
        pass

    @staticmethod
    def print_result(value):
        print()
        print()
        print(f'//========== {value} ==========//')
        print()

    @staticmethod
    def ynq_user_interaction(prompt_message):
        valid_responses = {'y', 'n', 'q'}  
        
        while True:
            user_input = input(prompt_message).lower()  
            
            if user_input in valid_responses:
                return user_input  
            elif user_input == 'q':
                break
            else:
                print("Error. Invalid input, please try again. ['Y/y' for Yes, 'N/n' for No, 'Q/q' for Quit]\n")

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
    def normalize_entry(entry_str:str) -> str:
        special_chars = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        remove_special_chars = re.sub(special_chars, '', entry_str.lower())
        normalized_str = re.sub(' ', '_', remove_special_chars)

        return normalized_str

    def main():
        auto = True
        answer_dic = App._user_inputs()

        App.print_result("DataIngestion processing...")
        project_data = mdls.DataIngestion.main(
            auto, 
            answer_dic["project_continuity"], 
            answer_dic["r_xlsx_file"], 
            answer_dic["r_xlsx_ws"],
            answer_dic["w_json_file"], 
            answer_dic["json_title"]
        )

        App.print_result("WbsFramework processing...")
        project_wbs = mdls.WbsFramework.main(
            auto, 
            answer_dic["project_continuity"], 
            answer_dic["r_xlsx_file"], 
            answer_dic["w_xlsx_ws"], 
            answer_dic["w_json_file"], 
            answer_dic["json_title"]
        )
        
        App.print_result("ScheduleFramework processing...")
        project_schdl = mdls.ScheduleFramework.main(
            auto, 
            answer_dic["r_xlsx_file"], 
            answer_dic["w_json_file"], 
            answer_dic["w_xlsx_ws"], 
            project_data["project_start_date"], 
            project_data["project_finish_date"], 
            answer_dic["json_title"]
        )
        
        # == WIP == #
        """ App.print_result("DataRelationship processing...")
        mdls.DataRelationship.main(auto, project) """

        App.print_result("LegendsFramework processing...")
        project_lgnds = mdls.LegendsFramework.main(
            auto, 
            answer_dic["r_xlsx_file"], 
            answer_dic["ws_legends"], 
            answer_dic["w_json_file"], 
            answer_dic["json_title"]
        )
            
        App.print_result("ExcelPostProcessing processing...")
        project_post = mdls.ExcelPostProcessing.main(
            auto, 
            answer_dic["r_xlsx_file"], 
            answer_dic["w_xlsx_ws"], 
            project_data["project_start_date"], 
            project_data["project_finish_date"],  
            answer_dic["w_json_file"], 
            answer_dic["json_title"]
        )

    def _user_inputs():
        process_continuity = input("Is this a completly new project? ")
        if process_continuity == 'q':
            print("Exiting the program.")
            return -1

        input_file_dir = input("Please enter the path to the file or directory to read: ").strip()
        output_file_dir = App.return_valid_path("Please enter the directory to save the new results package: ")
        input_project_code = input("Enter Project CODE: ").strip()
        input_project_title = input("Enter Project Title: ").strip()
        input_project_subtitle = input("Enter Project Subtitle: ").strip()
        input_project_client = input("Enter Project Client: ").strip()

        project_dic = {
            "project_continuity": process_continuity,
            "input_file": dict(
                path = os.path.dirname(input_file_dir),
                basename = os.path.basename(input_file_dir).split(".")[0],
                extension = os.path.basename(input_file_dir).split(".")[-1],
            ),
            "output_file": dict(
                path = os.path.dirname(output_file_dir),
                basename = os.path.basename(input_file_dir).split(".")[0],
                extension = os.path.basename(input_file_dir).split(".")[-1],
            ),
            "details": dict(
                project_dates = dict(
                    created = App.return_valid_date(),
                    updated = App.return_valid_date(),
                ),
                project_code = input_project_code,
                project_title = input_project_title,
                project_subtitle = input_project_subtitle,
                project_client = input_project_client,
            ),
        }

        return project_dic


if __name__ == "__main__":
    pass
