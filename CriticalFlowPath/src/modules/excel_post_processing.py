import os
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

class ExcelPostProcessing():
    def __init__(self, input_excel_path, input_excel_basename, input_worksheet_name):
        self.excel_path = input_excel_path
        self.excel_basename = input_excel_basename
        self.ws_name = input_worksheet_name
        self.wbs_start_row = 4
        self.wbs_start_col = 'A'
        self.trade_list_validation = [
            'Bricklayer',
            'Carpenter',
            'Cement Mason',
            'Drywall Finisher',
            'Electrician',
            'Elevator Constructor',
            'Glazier',
            'Insulation Worker',
            'Ironworker',
            'Laborer',
            'Millwright',
            'N/A',
            'Operating Engineer',
            'Painter',
            'Pipefitter',
            'Roofer',
            'Sheet Metal Worker',
            'Plumber'
        ]
        self.phase_list_validation = [
            'Civil',
            'Comissioning',
            'Elevator',
            'Exteriors/Skin',
            'Foundations',
            'Framing Structure',
            'Garage',
            'Interior Finishes',
            'Interior Rough Ins',
            'Landscaping Decks',
            'N/A',
            'Roof',
            'Site Prep',
            'Site Utilities',
            'Structure',
            'Transformer Vault'
        ]
        self.scope_of_work_list_validation = [
            'Construction',
            'Concrete Works', 
            'Demolition',  
            'Electrical',
            'Finishes',
            'Framing',
            'HVAC',  
            'Insulation',  
            'Landscaping',  
            'N/A',
            'Painting',  
            'Paving',  
            'Plumbing',
            'Roofing',  
            'Site Work',
            'Structural Steel'
        ]
    
    @staticmethod
    def main(auto=True, input_file_path=None, input_worksheet_name=None):
        if auto:
            project = ExcelPostProcessing.auto_generate_ins(input_file_path, input_worksheet_name)
        else:
            project = ExcelPostProcessing.generate_ins()

        active_workbook, active_worksheet = project.return_excel_workspace(project.ws_name)
        
        if active_workbook and active_worksheet:
            project.process_file()

    @staticmethod
    def generate_ins():
        input_file_path = input("Please enter the path to the Excel file or directory: ")
        input_excel_path, input_excel_basename = ExcelPostProcessing.file_verification(
            input_file_path, 'e', 'u')
        
        if input_excel_path == -1:
            return None  

        input_worksheet_name = input("Please enter the name to create a worksheet: ")

        return ExcelPostProcessing(input_excel_path, input_excel_basename, input_worksheet_name)

    @staticmethod
    def auto_generate_ins(input_file_path, input_worksheet_name):
        input_excel_path, input_excel_basename = ExcelPostProcessing.file_verification(
            input_file_path, 'e', 'u')
        
        if input_excel_path == -1:
            return None  

        return ExcelPostProcessing(input_excel_path, input_excel_basename, input_worksheet_name)

    @staticmethod
    def file_verification(input_file_path, file_type, mode):
        if os.path.isdir(input_file_path):
            file_path, file_basename = ExcelPostProcessing.handle_dir(input_file_path, mode)
            if mode != 'c':
                path, basename = ExcelPostProcessing.handle_file(file_path, file_basename, file_type)
            else:
                path = file_path
                basename = file_basename
        elif os.path.isfile(input_file_path):
            file_path = os.path.dirname(input_file_path)
            file_basename = os.path.basename(input_file_path)
            path, basename = ExcelPostProcessing.handle_file(file_path, file_basename, file_type)

        return path, basename
    
    @staticmethod
    def handle_dir(input_path, mode):
        if mode in ['u', 'r', 'd']:
            dir_list = os.listdir(input_path)
            selection = ExcelPostProcessing.display_directory_files(dir_list)
            base_name = dir_list[selection]
            print(f'File selected: {base_name}\n')
        elif mode == 'c':
            base_name = None
        else:
            print("Error: Invalid mode specified.")
            return -1
        
        return input_path, base_name

    @staticmethod
    def handle_file(file_path, file_basename, file_type):
        file = os.path.join(file_path, file_basename)

        if (file_type == 'e' and ExcelPostProcessing.is_xlsx(file)) or \
           (file_type == 'j' and ExcelPostProcessing.is_json(file)):
            return os.path.dirname(file), os.path.basename(file)
        
        print("Error: Please verify that the directory and file exist and that the file is of type .xlsx or .json")
        return -1

    @staticmethod
    def display_directory_files(list):
        selection_idx = 0
        if len(list)==0:
            print("Error. No files found")
            return -1
        
        if len(list)>1:
            print(f"-- {len(list)} files found:")
            idx = 0
            for file in list:
                idx += 1
                print(f"{idx}. {file}")

            selection_idx = input("\nPlease enter the index number to select the one to process: ") 
        else:
            print(f"Single file found: {list[0]}")
            print("Will go ahead and process")

        return int(selection_idx) - 1

    @staticmethod
    def is_xlsx(file_name):
        if file_name.endswith('.xlsx'):
            return True
        else:
            print('Error. Selected file is not an Excel')
            return False

    def return_excel_workspace(self, worksheet_name):
        file = os.path.join(self.excel_path, self.excel_basename)
        
        try:
            workbook = load_workbook(filename=file)
            worksheet = workbook[worksheet_name]
        except KeyError:
            print(f"Error: Worksheet '{worksheet_name}' does not exist.")
            
            while True:
                user_answer = input("Would you like to create a new worksheet under this name? (Y/N/Q): ").strip().lower()
                
                if user_answer == 'y':
                    worksheet = workbook.create_sheet(worksheet_name)
                    self.ws_name = worksheet_name
                    print(f"New worksheet '{self.ws_name}' created.\n")
                    break
                elif user_answer == 'n':
                    ws_list = workbook.sheetnames
                    selected_ws_idx = ExcelPostProcessing.display_directory_files(ws_list)
                    
                    if selected_ws_idx >= 0:  
                        worksheet = workbook.worksheets[selected_ws_idx]
                        self.ws_name = ws_list[selected_ws_idx]
                        print(f"Worksheet selected: '{self.ws_name}'\n")
                        return workbook, worksheet
                    else:
                        print("Invalid selection. Returning without changes.\n")
                        return workbook, None
                        
                elif user_answer == 'q':
                    print("Quitting without changes.")
                    return workbook, None
                else:
                    print("Invalid input. Please enter 'Y' for Yes, 'N' for No, or 'Q' to Quit.")
        
        return workbook, worksheet

    def process_file(self):
        print(f"Processing Excel file: {self.excel_basename}")
        """ self.validate_columns('scope_of_work')
        self.validate_columns('phase')
        self.validate_columns('trade')
        self.apply_post_processing() """

        self.apply_post_sectioning('location')

    def validate_columns(self, header):
        file = os.path.join(self.excel_path, self.excel_basename)
        workbook = load_workbook(filename=file)
        ws = workbook[self.worksheet_name]

        first_row = ws[self.wbs_start_row ]  
        
        if first_row is None:
            print("Error: The first row is empty.")
            return

        if header == 'scope_of_work':
            validation_list = self.scope_of_work_list_validation
        elif header == 'phase':
            validation_list = self.phase_list_validation
        elif header == 'trade':
            validation_list = self.trade_list_validation
        else:
            print(f"Error: Invalid header '{header}'. Supported headers are 'scope_of_work', 'phase', and 'trade'.")
            return
        
        header_columns = [col for col in first_row if col.value and header.lower() in str(col.value).lower()]

        if not header_columns:
            print(f"No columns found matching header: '{header}'")
            return

        for col in header_columns:
            col_index = col.column  

            dv = DataValidation(
                type='list',
                formula1=f'"{",".join(validation_list)}"',
                allow_blank=True
            )
            dv.error = 'Your entry is not in the list'
            dv.errorTitle = 'Invalid Entry'
            dv.prompt = 'Please select from the list'
            dv.promptTitle = 'List Selection'
            
            ws.add_data_validation(dv)
            
            dv.add(f'{get_column_letter(col_index)}2:{get_column_letter(col_index)}{ws.max_row}')
        
        workbook.save(file)
        print(f"Data validation applied to columns matching '{header}' successfully.")
        workbook.close()

    def apply_post_processing(self):
        file = os.path.join(self.file_path, self.file_basename)
        workbook = load_workbook(filename=file)
        ws = workbook[self.worksheet_name]

        first_row = ws[self.wbs_start_row ]
        
        if first_row is None:
            print("Error: The first row is empty.")
            return
        
        for cell in first_row:  
            cell.font = Font(name='Century Gothic', size=12, bold=True, color="FFFFFF")  
            cell.fill = PatternFill(start_color="00800080", end_color="00800080", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")  
        
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)  
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 1)  
            ws.column_dimensions[column_letter].width = adjusted_width

        for row in ws.rows:    
            if isinstance(row[0].value, int):
                parent_row = row
                for cell in parent_row:
                    cell.font = Font(name='Century Gothic', size=12, bold=True, color="00333333")  
                    cell.fill = PatternFill(start_color="00FFFFFF", end_color="00FFFFFF", fill_type="solid")
                    thin = Side(border_style="thin", color="000000")
                    cell.border = Border(bottom=thin)

        workbook.save(file)
        print(f"Post-processing completed. Saved to {file}")
        workbook.close()

    def apply_post_sectioning(self, section_header):
        file = os.path.join(self.excel_path, self.excel_basename)
        workbook = load_workbook(filename=file)
        ws = workbook[self.ws_name]

        header_idx = self.find_column_idx(ws, section_header)
        finish_idx = self.find_column_idx(ws, 'finish')

        section_list = self.list_cell_values(ws, header_idx)
        last_valid_section = section_list[0]

        for row_idx, row in enumerate(ws.iter_rows(min_col=finish_idx + 1, max_col=ws.max_column, min_row=self.wbs_start_row + 1, max_row=ws.max_row)):
            current_section = section_list[row_idx]

            if current_section and current_section != last_valid_section:
                self.style_row_border(ws, row)
                last_valid_section = current_section

        workbook.save(filename=file)
        print("Post sectioning applied successfully.")

    def style_row_border(self, active_ws, row):
        new_top_border = Side(border_style='dashed', color='000000')

        for cell in row:
            current_border = cell.border if cell.border else Border()
            new_border = Border(
                top=new_top_border, 
                left=current_border.left,  
                right=current_border.right,  
                bottom=current_border.bottom  
            )

            cell.border = new_border

    def list_cell_values(self, active_ws, col_idx):
        ws = active_ws
        col_list = []

        if col_idx is not None:
            for row in ws.iter_rows(min_row=self.wbs_start_row + 1, min_col=col_idx, 
                                    max_col=col_idx, max_row=ws.max_row):
                for cell in row:
                    col_list.append(cell.value)
        
        return col_list 

    def find_column_idx(self, active_ws, column_header):
        ws = active_ws
        start_col_idx = column_index_from_string(self.wbs_start_col)
        normalized_header = column_header.replace(" ", "_").lower()

        for row in ws.iter_rows(min_row=self.wbs_start_row, min_col=start_col_idx, max_col=ws.max_column):
            for cell in row:
                if cell.value and isinstance(cell.value, str):
                    normalized_cell_value = cell.value.replace(" ", "_").lower()
                    if normalized_header in normalized_cell_value:
                        return cell.column

if __name__ == "__main__":
    ExcelPostProcessing.main(False)
