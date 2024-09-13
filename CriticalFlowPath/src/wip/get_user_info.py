import os

file_path = "/home/coffee_6ean/Linux/CriticalFlowPath/results/excel"

class GetUserInfo(file_path):
    def __init__(self, dir_path, file_name, worksheet_name, start_row, start_col, start_date, end_date):
        self.dir_path = dir_path
        self.file_name = file_name
        self.worksheet_name = worksheet_name
        self.start_row = start_row
        self.start_col = start_col
        self.start_date = start_date
        self.end_date = end_date
    
    @staticmethod
    def main():
        GetUserInfo.get_input()
        project = GetUserInfo(input_dir_path, input_file_name, input_worksheet_name, input_start_row, input_start_col, input_start_date, input_end_date)

    @staticmethod
    def display_directory_files(list):
        selection_idx = 0
        if len(list)==0:
            print('Error. No files found')
            return -1
        
        if len(list)>1:
            print(f'{len(list)} files found:')
            idx = 0
            for file in list:
                idx += 1
                print(f'{idx}. {file}')

            selection_idx = input('\nPlease enter the index number to select the one to process: ') 
        else:
            print(f'Single file found: {list[0]}')
            print('Will go ahead and process')

        return int(selection_idx) - 1

    def ask_user_input(self, inter_type):
        input_dic = self.questions_dic["input_txt"]
        user_input = []
        for question in input_dic.keys():
            user_input.append()

        question_prompt = input('Please enter the pdf file path to read: ')

        return question_prompt

    def file_verification(self):
        file_path = self.pdf_file_path

        if os.path.isdir(file_path):
            file_list = os.listdir(file_path)
            selection = GetUserInfo.display_directory_files(file_list)

            file_name = file_list[selection]

            print(f'File selected: {file_name}')
            file = os.path.join(file_path, file_name)
            if GetUserInfo.is_pdf(file):
                return file
            else:
                return -1
        elif os.path.isfile(file_path):
            if GetUserInfo.is_pdf(file_path):
                return file_path
            else:
                return -1
        else: 
            print('Error. Please verify the directory and file exist and that the file is of type .pdf')    
            return -1

    def questions_dic(self):
        user_inter_dic = {
            "input": {
                "json": {
                    "askFor_file_path": "Please enter the path to the JSON file or directory: ",
                    "askFor_file_name": "Please enter the file name to save (without extension): ",
                    "askFor_start_date": "Please enter the start date for the schedule (format: dd-MMM-yy): ",
                    "askFor_end_date": "Please enter the end date for the schedule (format: dd-MMM-yy): ",
                },
                "pdf": {
                    "askFor_file_path": "Please enter the path to the PDF file or directory: ",
                    "askFor_file_name": "Please enter the file name to save (without extension): ",
                    "askFor_initial_tag": "Please enter the initial anchor tag: ",
                    "askFor_final_tag": "Please enter the final anchor tag: ",
                },
                "xlsx": {
                    "askFor_file_path": "Please enter the path to the Excel file or directory: ",
                    "askFor_file_name": "Please enter the file name to save (without extension): ",
                    "askFor_initial_tag": "Please enter the initial anchor tag: ",
                    "askFor_final_tag": "Please enter the final anchor tag: ",
                    "askFor_start_row": "Please enter the starting row to write the schedule: ",
                    "askFor_start_col": "Please enter the starting column to write the schedule: ",
                    "askFor_worksheet_name": "Please enter the name for the new or existing worksheet: ",
                },
            },
            "output": {
                "json": {
                    "askFor_file_path": "Please enter the directory path to save the JSON file: ",
                    "askFor_file_name": "Please enter the file name to save (without extension): ",
                    "askFor_worksheet_name": "Please enter the name for the new or existing worksheet: ",
                },
                "pdf": {
                    "askFor_file_path": "Please enter the directory path to save the PDF file: ",
                    "askFor_file_name": "Please enter the file name to save (without extension): ",
                },
                "xlsx": {
                    "askFor_file_path": "Please enter the directory path to save the Excel file: ",
                    "askFor_file_name": "Please enter the file name to save (without extension): ",
                    "askFor_worksheet_name": "Please enter the name for the new or existing worksheet: ",
                },
            }
        }

        return user_inter_dic

if __name__ == "__main__":
    pass