import os
import subprocess
import configparser

import sys
sys.path.append("../")
from CpmProcessor.keys.secrets import DB_CONFIG, DB_SETUP, DB_SCHEMA_AUTH, DB_SCHEMA_CONSTRUCTION, DB_SCHEMA_SHARED, DB_SCHEMA_SYSTEM

class Initialize:
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
        project = Initialize.generate_ins()

        if project:
            config = Initialize.load_config(DB_CONFIG)

            if config:                
                if Initialize.initialize_database(config):
                    env = os.environ.copy()
                    env["PGPASSWORD"] = config["postgresql"]["password"]

                    for _, file_path in project.db_build_heirarchy.items():
                        sql_file = f"{file_path}/{project.initizalize_file_title}"
                        subprocess.run(
                            [
                                "psql",
                                "-U", config["postgresql"]["user"],
                                "-h", "localhost",
                                "-p", config["postgresql"]["port"],
                                "-f", sql_file
                            ],
                            env=env,
                            check=True
                        )

    @staticmethod
    def generate_ins():
        ins = Initialize()

        return ins

    @staticmethod
    def load_config(path:str):
        config = configparser.ConfigParser()
        config.read(path)

        return config

    @staticmethod
    def initialize_database(db_config) -> str:
        sql_code = Initialize._render_template(DB_SETUP, {"db_name": db_config["postgresql"]["dbname"]})
        tmp_file_path = Initialize.create_temp_sql_file("db.sql", sql_code)
        
        if Initialize._save_and_run(sql_code, db_config, tmp_file_path):
            print(f"Successfully initialized database: {db_config['postgresql']['dbname']}")
        else:
            print(f"Error. Database {db_config['postgresql']['dbname']} not found after execution")

        return tmp_file_path

    @staticmethod
    def _render_template(sql_setup_path:str, replacements:dict) -> str:
        with open(sql_setup_path, 'r') as read_file:
            sql_setup_script = read_file.read()

        for key, value in replacements.items():
            sql = sql_setup_script.replace(key, value)

        return sql
    
    @staticmethod
    def create_temp_sql_file(output_file_basename:str, content:str) -> str:
        current_working_dir = os.getcwd()

        if '.' in output_file_basename:
            tmp_output_basename= output_file_basename.split('.')[0]
        else:
            tmp_output_basename = output_file_basename
        
        tmp_output_file = f"{current_working_dir}/{tmp_output_basename}.sql"

        with open(tmp_output_file, 'w') as file:
            file.write(content)

        return tmp_output_file

    @staticmethod
    def _save_and_run(sql_code:str, db_config, output_path:str) -> bool:
        if output_path:
            with open(output_path, 'w') as f:
                f.write(sql_code)

        env = os.environ.copy()
        env["PGPASSWORD"] = db_config["postgresql"]["password"]

        # Run SQL file
        subprocess.run(
            [
                "psql",
                "-U", db_config["postgresql"]["user"],
                "-h", "localhost",
                "-p", db_config["postgresql"].get("port", "5432"),
                "-f", output_path
            ],
            env=env,
            check=True
        )

        # List databases
        result = subprocess.run(
            [
                "psql",
                "-U", db_config["postgresql"]["user"],
                "-h", "localhost",
                "-p", db_config["postgresql"].get("port", "5432"),
                "-l"
            ],
            env=env,
            capture_output=True,
            text=True
        )

        if db_config["postgresql"]["dbname"] in result.stdout:
            return True

        return False

    @staticmethod
    def clean_up(file_list:list):
        pass


if __name__ == "__main__":
    Initialize.main()