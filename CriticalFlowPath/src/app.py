import os
from datetime import datetime
import modules

def print_result(value):
    print()
    print()
    print(f'//========== {value} ==========//')
    print()

def system_cfa_creation():
    print_result("PdfToJson processing...")
    modules.PdfToJson.main()
    print_result("JsonToExcel processing...")
    modules.JsonToExcel.main()
    print_result("ExcelPostProcessing processing...")
    modules.ExcelPostProcessing.main()
    print_result("ScheduleFramework processing...")
    modules.ScheduleFramework.main()
    print_result("End")

def system_cfa_update():
    auto = True
    answer_dic = user_inputs()

    print_result("FilledExcelToUpdateJson processing...")
    modules.FilledExcelToUpdateJson.main(auto, answer_dic["proc_cont"], answer_dic["xlsx_file"], 
                                         answer_dic["ws_read"], answer_dic["json_file"])
    print_result("WbsFramework processing...")
    modules.WbsFramework.main(auto, answer_dic["proc_cont"], answer_dic["xlsx_file"], 
                              answer_dic["ws_schedule"], answer_dic["json_file"])
    print_result("ScheduleFramework processing...")
    modules.ScheduleFramework.main(auto, answer_dic["xlsx_file"], answer_dic["ws_schedule"], 
                                   answer_dic["start_date"], answer_dic["end_date"])
    print_result("LegendsFramework processing...")
    modules.LegendsFramework.main(auto, answer_dic["xlsx_file"], answer_dic["ws_legends"], answer_dic["json_file"])
    print_result("ExcelPostProcessing processing...")
    modules.ExcelPostProcessing.main(auto, answer_dic["xlsx_file"], answer_dic["ws_schedule"])

def user_inputs():
    process_continuity = input("Is this a completly new project? ")
    if process_continuity == 'q':
        print("Exiting the program.")
        return -1
    
    now = add_date()

    input_excel_dir = input("Please enter the path to the Excel file or directory: ")
    input_worksheet_read = input("Please enter the name for the worksheet to read: ")
    input_worksheet_schedule = input("Please enter the name for the new worksheet (WBS + Schedule): ")
    input_worksheet_legends = input("Please enter the name for the new worksheet (Legends): ")
    input_json_dir = input("Please enter the directory to save the new JSON file: ")
    input_json_name = input("Please enter the name for the new JSON file (Base Style): ")
    input_start_date = input("Please enter the start date of the project (format: dd-MMM-yyyy): ")
    input_end_date = input("Please enter the end date of the project (format: dd-MMM-yyyy): ")

    answer_dic = {
        "proc_cont": process_continuity,
        "xlsx_file": input_excel_dir,
        "ws_read": input_worksheet_read,
        "ws_schedule": input_worksheet_schedule,
        "ws_legends": input_worksheet_legends,
        "json_file": input_json_dir,
        "json_name": input_json_name,
        "start_date": input_start_date,
        "end_date": input_end_date
    }

    return answer_dic

def add_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    return dt_string


if __name__ == "__main__":
    #system_pdf_to_excel_gantt()
    system_cfa_update()
