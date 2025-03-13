import psycopg
from psycopg import sql

import sys
sys.path.append('../')
from CpmProcessor.src.db.utils.load_db import load_config

class Versions:

    SCHEMA = "cpm_schema"
    TABLE = "versions"

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_column_names() -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT COLUMN_NAME
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;
                    """)

                    cur.execute(query, (Versions.SCHEMA, Versions.TABLE))

                    available_columns = [row[0] for row in cur.fetchall()]
                    return available_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving project columns: {e}")
            return []

    @staticmethod
    def get_none_nullable_columns() -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT COLUMN_NAME
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND IS_NULLABLE = 'NO';
                    """)

                    cur.execute(query, (Versions.SCHEMA, Versions.TABLE))

                    nullable_columns = [row[0] for row in cur.fetchall()]
                    return nullable_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving nullable columns: {e}")
            return []

    @staticmethod
    def create(**version:dict) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = version.keys()
                    values = [version[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.{} ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Versions.SCHEMA),
                        sql.Identifier(Versions.TABLE),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    version_id = cur.fetchone()[0]
                    conn.commit()
                    return version_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating version: {e}")
            conn.rollback()
            return None

    @staticmethod
    def read(version_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Versions.SCHEMA),
                        sql.Identifier(Versions.TABLE)
                    )

                    cur.execute(query, (version_id,))

                    row = cur.fetchone()

                    if row:
                        column_names = [desc[0] for desc in cur.description]
                        version = dict(zip(column_names, row))
                        return version
                    else:
                        return {}
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error reading version: {e}")
            return {}

    @staticmethod
    def read_all() -> list|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT * FROM {}.{};").format(
                        sql.Identifier(Versions.SCHEMA),
                        sql.Identifier(Versions.TABLE)
                    )

                    cur.execute(query)
                    return cur.fetchall()
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Versions.SCHEMA}.{Versions.TABLE}: {e}")
            return None

    @staticmethod
    def search_by(value:str, category:str) -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE {} ILIKE %s;
                    """).format(
                        sql.Identifier(Versions.SCHEMA),
                        sql.Identifier(Versions.TABLE),
                        sql.Identifier(category)
                    )

                    cur.execute(query, (f"%{value}%",))

                    rows = cur.fetchall()

                    versions = []
                    column_names = [desc[0] for desc in cur.description]
                    for row in rows:
                        versions.append(dict(zip(column_names, row)))

                    return versions
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error searching for version: {e}")
            return []    

    @staticmethod
    def update(version_id:int, **version_update) -> bool:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = version_update.keys()
                    values = [version_update[column] for column in columns]
                    values.append(version_id)

                    query = sql.SQL("""
                        UPDATE {}.{}
                        SET {}, updated_at = NOW()
                        WHERE id = %s
                        RETURNING *;
                    """).format(
                        sql.Identifier(Versions.SCHEMA),
                        sql.Identifier(Versions.TABLE),
                        sql.SQL(', ').join(sql.SQL("{} = {}").join(
                            map(sql.Identifier(column), sql.Placeholder(column)) for column in columns
                        ))
                    )

                    cur.execute(query, values)

                    updated_activity = cur.fetchone()
                    conn.commit()

                    if updated_activity:
                        print(f"Version with ID {version_id} updated successfully.")
                        print("Updated version:", updated_activity)
                        return True
                    else:
                        print(f"No version found with ID {version_id}.")
                        return False
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error updating version {version_id}: {e}")
            conn.rollback()
            return False
    
    @staticmethod
    def delete(version_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    version = Versions.read(version_id)
                    if not version:
                        print(f"Version with ID {version_id} not found.")
                        return {}

                    query = sql.SQL("""
                        DELETE FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Versions.SCHEMA),
                        sql.Identifier(Versions.TABLE)
                    )

                    cur.execute(query, (version_id,))

                    conn.commit()

                    print(f"Version with ID {version_id} deleted successfully.")
                    return version  
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error deleting version {version_id}: {e}")
            return {}


if __name__ == "__main__":
    pass
