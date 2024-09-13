import os
import modules

def print_result(value):
    print()
    print()
    print(f'//----------------- {value} -----------------//')
    print()

def system_pdf_to_excel_gantt():
    print_result("PdfToJson processing...")
    modules.PdfToJson.main()
    print_result("JsonToExcel processing...")
    modules.JsonToExcel.main()
    print_result("ExcelPostProcessing processing...")
    modules.ExcelPostProcessing.main()
    print_result("ScheduleFramework processing...")
    modules.ScheduleFramework.main()
    print_result("End")


if __name__ == "__main__":
    system_pdf_to_excel_gantt()
