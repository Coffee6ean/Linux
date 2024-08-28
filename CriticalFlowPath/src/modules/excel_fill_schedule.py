import os
from datetime import datetime, timedelta
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

class FillSchedule:
    def __init__(self, input_file_path=None, start_row=None, start_col=None, start_date=None, end_date=None):
        self.input_file_path = input_file_path
        self.start_row = int(start_row) if start_row else None
        self.start_col = int(start_col) if start_col else None
        self.start_date = start_date
        self.end_date = end_date

    def main(self):
        #WIP
        pass

    def generate_body_schedule(self, workbook, worksheet, start_date, end_date):
        #WIP
        pass

if __name__ == "__main__":
    pass