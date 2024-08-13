from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill
from pdf_to_jason import print_result

class ExcelPostProcessing:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.list_validation = [
            'Carpenter',
            'Electrician',
            'Plumber',
            'Ironworker',
            'Sheet Metal Worker',
            'Pipefitter',
            'Laborer',
            'N/A',
            'Operating Engineer',
            'Bricklayer',
            'Cement Mason',
            'Roofer',
            'Glazier',
            'Painter',
            'Drywall Finisher',
            'Insulation Worker',
            'Elevator Constructor',
            'Millwright'
        ]

    def apply_post_processing(self):
        """
        Applies styling and data validation to the Excel workbook.
        """
        workbook = load_workbook(filename=self.input_file_path)
        ws = workbook['Project Content']

        # Apply data validation to 'trade' columns
        trade_columns = [col for col in ws['1'] if 'trade' in col.value]
        for col in trade_columns:
            col_index = col.column  # Get the index of the column (1-based)
            dv = DataValidation(type='list', formula1=f'"{",".join(self.list_validation)}"', allow_blank=True)
            dv.error = 'Your entry is not in the list'
            dv.errorTitle = 'Invalid Entry'
            dv.prompt = 'Please select from the list'
            dv.promptTitle = 'List Selection'
            ws.add_data_validation(dv)
            dv.add(f'{get_column_letter(col_index)}2:{get_column_letter(col_index)}{ws.max_row}')

        # Style the header row
        for cell in ws['1']:  # Assuming the first row contains headers
            cell.font = Font(bold=True, color="FFFFFF")  # Bold and white font
            cell.fill = PatternFill(start_color="00993366", end_color="00993366", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")  # Center alignment

        # Adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)  # Get the column letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)  # Add some padding
            ws.column_dimensions[column_letter].width = adjusted_width

        workbook.save(self.input_file_path)
        print(f"Post-processing completed. Saved to {self.input_file_path}")
        workbook.close()

if __name__ == "__main__":
    post_processing = ExcelPostProcessing('/home/coffee_6ean/Linux/CriticalFlowPath/results/excel/test.xlsx')
    post_processing.apply_post_processing()