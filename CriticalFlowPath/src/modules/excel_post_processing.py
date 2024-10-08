import os
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

class ExcelPostProcessing():
    def __init__(self, input_file_path, input_file_basename, xlsx_worksheet_name):
        self.file_path = input_file_path
        self.file_basename = input_file_basename
        self.worksheet_name = xlsx_worksheet_name
        self.starting_data_row = 4
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
    def main():
        project = ExcelPostProcessing.generate_ins()
        project.process_file()

    @staticmethod
    def generate_ins():
        input_file_path = input("Please enter the path to the Excel file or directory: ")
        input_path, input_base_name = ExcelPostProcessing.file_verification(input_file_path)
        if input_path == -1:
            return None  

        xlsx_worksheet_name = input("Please enter the name to create a worksheet: ")

        return ExcelPostProcessing(input_path, input_base_name, xlsx_worksheet_name)

    @staticmethod
    def file_verification(input_file_path):
        if os.path.isdir(input_file_path):
            path = input_file_path
            dir_list = os.listdir(path)
            selection = ExcelPostProcessing.display_directory_files(dir_list)

            base_name = dir_list[selection]

            print(f'File selected: {base_name}')
            file = os.path.join(path, base_name)
            if ExcelPostProcessing.is_xlsx(file):
                return path, base_name
            else:
                return -1
        elif os.path.isfile(input_file_path):
            if ExcelPostProcessing.is_xlsx(input_file_path):
                path = os.path.dirname(input_file_path)
                base_name = os.path.basename(input_file_path)
                return path, base_name
            else:
                return -1
        else: 
            print('Error. Please verify the directory and file exist and that the file is of type .xlsx')    
            return -1

    @staticmethod
    def display_directory_files(list):
        selection_idx = 0
        if len(list)==0:
            print('Error. No files found')
            return -1
        
        if len(list)>1:
            print(f'-- {len(list)} files found:')
            idx = 0
            for file in list:
                idx += 1
                print(f'{idx}. {file}')

            selection_idx = input('\nPlease enter the index number to select the one to process: ') 
        else:
            print(f'Single file found: {list[0]}')
            print('Will go ahead and process')

        return int(selection_idx) - 1

    @staticmethod
    def is_xlsx(file_name):
        if file_name.endswith('.xlsx'):
            return True
        else:
            print('Error. Selected file is not an Excel')
            return False

    def process_file(self):
        print(f"Processing Excel file: {self.file_basename}")
        self.validate_columns('scope_of_work')
        self.validate_columns('phase')
        self.validate_columns('trade')
        self.apply_post_processing()

    def validate_columns(self, header):
        file = os.path.join(self.file_path, self.file_basename)
        workbook = load_workbook(filename=file)
        ws = workbook[self.worksheet_name]

        first_row = ws[self.starting_data_row]  
        
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

        first_row = ws[self.starting_data_row]
        
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


if __name__ == "__main__":
    ExcelPostProcessing.main()
