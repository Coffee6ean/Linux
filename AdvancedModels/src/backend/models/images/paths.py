import sys
import os

from ...lib.reusable_methods import get_file_path

INPUT_PATH = get_file_path('Input')
PROCESS_PATH = get_file_path('Process')
OUTPUT_PATH = get_file_path('Output')

if __name__ == '__main__':
    print('Input path:', INPUT_PATH)
