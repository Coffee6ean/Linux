import os
import re
from datetime import datetime
import modules as mdls

def print_result(value):
    print()
    print()
    print(f'//========== {value} ==========//')
    print()

def system_cfa_create():
    auto = True
    answer_dic = user_inputs()

    print_result("DataIngestion processing...")
    mdls.DataIngestion.main(auto, answer_dic["proc_cont"], answer_dic["xlsx_file"], answer_dic["ws_read"],
                               answer_dic["json_file"], answer_dic["json_title"])
    print_result("WbsFramework processing...")
    mdls.WbsFramework.main(auto, answer_dic["proc_cont"], answer_dic["xlsx_file"], 
                              answer_dic["ws_schedule"], answer_dic["json_file"], answer_dic["json_title"])
    print_result("ScheduleFramework processing...")
    project = mdls.ScheduleFramework.main(auto, answer_dic["xlsx_file"], answer_dic["json_file"], answer_dic["ws_schedule"], 
                                   answer_dic["start_date"], answer_dic["end_date"], answer_dic["json_title"])
    # == WIP == #
    """ print_result("DataRelationship processing...")
    mdls.DataRelationship.main(auto, project) """

    print_result("LegendsFramework processing...")
    mdls.LegendsFramework.main(auto, answer_dic["xlsx_file"], answer_dic["ws_legends"], 
                                  answer_dic["json_file"], answer_dic["json_title"])
    print_result("ExcelPostProcessing processing...")
    mdls.ExcelPostProcessing.main(auto, answer_dic["xlsx_file"], answer_dic["ws_schedule"], 
                                     answer_dic["start_date"], answer_dic["end_date"], 
                                     answer_dic["json_file"], answer_dic["json_title"])

def user_inputs():
    process_continuity = input("Is this a completly new project? ")
    if process_continuity == 'q':
        print("Exiting the program.")
        return -1
    
    now = add_date()

    input_excel_dir = input("Please enter the path to the Excel file or directory: ").strip()
    input_worksheet_read = input("Please enter the name for the worksheet to read: ").strip()
    input_worksheet_schedule = input("Please enter the name for the new worksheet (WBS + Schedule): ").strip()
    input_worksheet_legends = input("Please enter the name for the new worksheet (Legends): ").strip()
    input_json_dir = input("Please enter the directory to save the new JSON file: ").strip()
    input_json_title = input("Please enter the name for the new JSON file (Base Style): ").strip()
    input_start_date = return_valid_date("Please enter the start date of the project (format: dd-MMM-yyyy): ")
    input_end_date = return_valid_date("Please enter the end date of the project (format: dd-MMM-yyyy): ")

    answer_dic = {
        "proc_cont": process_continuity,
        "xlsx_file": input_excel_dir,
        "ws_read": input_worksheet_read,
        "ws_schedule": input_worksheet_schedule,
        "ws_legends": input_worksheet_legends,
        "json_file": input_json_dir,
        "json_title": input_json_title,
        "start_date": input_start_date,
        "end_date": input_end_date
    }

    return answer_dic

def add_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    return dt_string

def return_valid_date(message):
    while(True):   
        value = input(message).strip()
        try:
            if datetime.strptime(value, "%d-%b-%Y"):
                return value
        except Exception as e:
            print(f"Error. {e}\n")

def normalize_entry(entry_str):
    special_chars = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    remove_special_chars = re.sub(special_chars, '', entry_str.lower())
    normalized_str = re.sub(' ', '_', remove_special_chars)

    return normalized_str

if __name__ == "__main__":
    system_cfa_create()
