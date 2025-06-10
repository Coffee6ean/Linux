import os
import psycopg2
import argparse

import sys
sys.path.append("../")

class Seed:
    def __init__(self, credentials_name=None, credentials_user=None, credentials_host=None, 
                 credentials_port=None, credentials_psswd=None):
        self.db_cred_name = credentials_name
        self.db_cred_user = credentials_user
        self.db_cred_host = credentials_host
        self.db_cred_port = credentials_port
        self.db_cred_psswd = credentials_psswd
        

    @staticmethod
    def main():
        pass

    @staticmethod
    def generate_ins():
        pass

    @staticmethod
    def connect_to_db():
        pass

    @staticmethod
    def seed_table(db, schema, table, seed_dict):
        pass

if __name__ == "__main__":
    pass