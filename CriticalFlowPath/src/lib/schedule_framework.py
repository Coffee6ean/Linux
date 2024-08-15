from datetime import datetime, timedelta
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

class ScheduleFramework:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path

    def same_cell_values(self, row_idx):
        # Load the workbook and select the relevant worksheet
        workbook = load_workbook(filename=self.input_file_path)
        worksheet = workbook['Gantt Schedule']

        first_row = worksheet[row_idx]  # Access the first row
        last_value = first_row[0].value  # Store the value of the first cell
        same_cell_list = []  # List to hold cells with the same values
        overall_list = []  # List to hold all groups of same-value cells

        for cell in first_row:
            if cell.value == last_value:  # Check if the current cell matches the last value
                same_cell_list.append(cell.column)  # Append the column index to the list
            else:
                if same_cell_list:  # If we have collected cells, append to overall_list
                    overall_list.append(same_cell_list)
                same_cell_list = [cell.column]  # Start a new list with the current cell's column
                last_value = cell.value  # Update last_value to the current cell's value

        # Append the last collected same-value cells if any
        if same_cell_list:
            overall_list.append(same_cell_list)

        return overall_list, row_idx  # Return the overall list of same-value cells & row index

    def merge_same_value_cells(self, column_indices, row_idx):
        # Load the workbook and select the relevant worksheet
        workbook = load_workbook(filename=self.input_file_path)
        worksheet = workbook['Gantt Schedule']

        # Ensure there are column indices to merge
        if not column_indices:
            print("No columns to merge.")
            return

        # Get the first and last columns to merge
        first_col = column_indices[0]
        last_col = column_indices[-1]

        # Merge the cells in the specified row
        worksheet.merge_cells(start_row=row_idx, start_column=first_col, end_row=row_idx, end_column=last_col)

        # Save the workbook after merging cells
        workbook.save(self.input_file_path)
        #print(f"Merged cells from column {first_col} to {last_col} in row {row_idx}.")
        workbook.close()

    def generate_gantt_schedule(self, start_date, end_date):
        # Load the workbook and create a new worksheet for the Gantt chart
        workbook = load_workbook(filename=self.input_file_path)
        worksheet = workbook.create_sheet('Gantt Schedule')

        # Convert string dates to datetime objects
        start_datetime_obj = datetime.strptime(start_date, '%d-%b-%y')
        end_datetime_obj = datetime.strptime(end_date, '%d-%b-%y')

        # Calculate the duration in days
        duration = (end_datetime_obj - start_datetime_obj).days + 1  # Include the end date

        # Fill the third row with days
        for day in range(duration):
            date = start_datetime_obj + timedelta(days=day)
            worksheet.cell(row=3, column=day + 1, value=date.strftime('%d'))

        # Fill the second row with months
        for day in range(duration):
            date = start_datetime_obj + timedelta(days=day)
            worksheet.cell(row=2, column=day + 1, value=date.strftime('%b'))

        # Fill the first row with years
        for day in range(duration):
            date = start_datetime_obj + timedelta(days=day)
            worksheet.cell(row=1, column=day + 1, value=date.strftime('%y'))
        
        # Save the workbook after generating the Gantt chart
        workbook.save(self.input_file_path)
        print("Gantt chart generated successfully.")
        workbook.close()
    
    def style_worksheet(self):
        workbook = load_workbook(filename=self.input_file_path)
        worksheet = workbook['Gantt Schedule']
    
        # Define the border style
        thin_border = Border(left=Side(style='thin'))
    
        # Apply the font style, center alignment, and fill color to the header row (first row)
        for cell in worksheet[1]:  # Assuming the first row is the header
            cell.font = Font(name='Century Gothic', size=12, bold=True, color="FFFFFF")  # Bold and white font
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.fill = PatternFill(start_color='00800080', end_color='00800080', fill_type='solid')
    
        # Apply the font style, center alignment, and fill color to the second row (months)
        for cell in worksheet[2]:  # Assuming the second row contains months
            cell.font = Font(name='Century Gothic', size=12, bold=True, color="00333333")
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.fill = PatternFill(start_color='00CC99FF', end_color='00CC99FF', fill_type='solid')
    
        # Apply the font style, center alignment, and fill color to the third row (days)
        for cell in worksheet[3]:  # Assuming the third row contains days
            cell.font = Font(name='Century Gothic', size=12, bold=True, color="00000000")
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.fill = PatternFill(start_color='00C0C0C0', end_color='00C0C0C0', fill_type='solid')
    
        # Apply styles to other rows and accentuate the left border
        for row in worksheet.iter_rows(min_row=4):  # Starting from the fourth row
            for cell in row:
                # Center align all cells
                cell.alignment = Alignment(horizontal='center', vertical='center')
    
         # Accent the left border for the last cell of each month
        last_month_col = 1  # Start from the first column
        for col in range(1, worksheet.max_column + 1):
            last_month_cell = worksheet.cell(row=2, column=col)  # Get the month cell
            if last_month_cell.value is not None:  # Only apply border if there is a value
                # Apply border to all rows in this column starting from the third row
                for row in range(3, worksheet.max_row + 1):  # Starting from the third row
                    cell = worksheet.cell(row=row, column=col)
                    cell.border = thin_border
                last_month_col = col  # Update last_month_col to the current column
    
        workbook.save(self.input_file_path)
        print("Workbook styled and saved successfully.")
        workbook.close()

if __name__ == "__main__":
    input_file_path = input("Please enter the folder path to the Excel file: ")
    gantt_schedule = ScheduleFramework(input_file_path)
    gantt_schedule.generate_gantt_schedule('17-Feb-23', '16-Jun-25')

    year_list, year_row = gantt_schedule.same_cell_values(1)
    for year in year_list:
        gantt_schedule.merge_same_value_cells(year, year_row)

    month_list, month_row = gantt_schedule.same_cell_values(2)
    for month in month_list:
        gantt_schedule.merge_same_value_cells(month, month_row)

    gantt_schedule.style_worksheet()
