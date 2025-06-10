import os
import psycopg2
import argparse

import sys
sys.path.append("../")

class Connect:
    def __init__(self, credentials_name=None, credentials_user=None, credentials_host=None, 
                 credentials_port=None, credentials_psswd=None):
        self.db_cred_name = credentials_name
        self.db_cred_user = credentials_user
        self.db_cred_host = credentials_host
        self.db_cred_port = credentials_port
        self.db_cred_psswd = credentials_psswd
        
    @staticmethod
    def main(credentials_name=None, credentials_user=None, 
             credentials_host=None, credentials_port=None, credentials_psswd=None):
        project = Connect.generate_ins(
            credentials_name,
            credentials_user,
            credentials_host,
            credentials_port,
            credentials_psswd
        )

        if project:
            return project.connect_to_db(
                credentials_name,
                credentials_user,
                credentials_host,
                credentials_port,
                credentials_psswd
            )

    @staticmethod
    def generate_ins(credentials_name=None, credentials_user=None,
                     credentials_host=None, credentials_port=None, credentials_psswd=None):
        ins = Connect(
            credentials_name,
            credentials_user,
            credentials_host,
            credentials_port,
            credentials_psswd
        )

        return ins

    @staticmethod
    def connect_to_db(credentials_name=None, credentials_user=None, 
             credentials_host=None, credentials_port=None, credentials_psswd=None):
        conn = None

        try:
            conn = psycopg2.connect(
                dbname=credentials_name,
                user=credentials_user,
                password=credentials_psswd,
                host=credentials_host,
                port=credentials_port
            )

            if conn is not None:
                print("Database connection succesfull")

        except Exception as e:
            print(f"Error: {e}")

        return conn

    @staticmethod
    def check_for_existing_connection(connection):
        try:
            cur = connection.cursor()
            cur.execute("SELECT * FROM pg_stat_activity WHERE datname = current_database();")
            rows = cur.fetchall()

            print(f"Currently connected to: {rows[0][1]}")
        except psycopg2.OperationalError:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="db>conn",
        description="Connect to database"
    )
    parser.add_argument("--name")
    parser.add_argument("--user")
    parser.add_argument("--host")
    parser.add_argument("--password")
    parser.add_argument("--port")
    args = parser.parse_args()

    db_conn = Connect.main(
        credentials_name=args.name,
        credentials_user=args.user,
        credentials_host=args.host,
        credentials_port=args.port,
        credentials_psswd=args.password
    )

    Connect.check_for_existing_connection(db_conn)
