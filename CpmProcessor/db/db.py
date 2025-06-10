import os
import subprocess
import configparser

import sys
sys.path.append("../")
from CpmProcessor.keys.secrets import DB_CONFIG, DB_SETUP, DB_SCHEMA_AUTH, DB_SCHEMA_CONSTRUCTION, DB_SCHEMA_SHARED, DB_SCHEMA_SYSTEM

class DataBase:
    def __init__(self):
        self.initizalize_file_title = "init.sql"
        self.db_build_heirarchy = {
            "system_schema": DB_SCHEMA_SYSTEM, 
            "shared_schema": DB_SCHEMA_SHARED, 
            "auth_schema": DB_SCHEMA_AUTH, 
            "construction_schema": DB_SCHEMA_CONSTRUCTION, 
        }

    @staticmethod
    def main():
        project = DataBase.generate_ins()


    @staticmethod
    def generate_ins():
        ins = DataBase()

        return ins

    @staticmethod
    def clean_up(file_list:list):
        pass


if __name__ == "__main__":
    DataBase.main()