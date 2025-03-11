import psycopg
from psycopg import sql

import sys
sys.path.append('../')
from CpmProcessor.src.db.utils.load_db import load_config

class Procurements:

    SCHEMA = "cpm_schema"
    TABLE = "procurements"

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

                    cur.execute(query, (Procurements.SCHEMA, Procurements.TABLE))

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

                    cur.execute(query, (Procurements.SCHEMA, Procurements.TABLE))

                    nullable_columns = [row[0] for row in cur.fetchall()]
                    return nullable_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving nullable columns: {e}")
            return []

    @staticmethod
    def create(**procurement:dict) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = procurement.keys()
                    values = [procurement[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.{} ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Procurements.SCHEMA),
                        sql.Identifier(Procurements.TABLE),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    procurement_id = cur.fetchone()[0]
                    conn.commit()
                    return procurement_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating procurement: {e}")
            conn.rollback()
            return None

    @staticmethod
    def read(procurement_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Procurements.SCHEMA),
                        sql.Identifier(Procurements.TABLE)
                    )

                    cur.execute(query, (procurement_id,))

                    row = cur.fetchone()

                    if row:
                        column_names = [desc[0] for desc in cur.description]
                        procurement = dict(zip(column_names, row))
                        return procurement
                    else:
                        return {}
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error reading procurement: {e}")
            return {}

    @staticmethod
    def read_all() -> list|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT * FROM {}.{};").format(
                        sql.Identifier(Procurements.SCHEMA),
                        sql.Identifier(Procurements.TABLE)
                    )

                    cur.execute(query)
                    return cur.fetchall()
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Procurements.SCHEMA}.{Procurements.TABLE}: {e}")
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
                        sql.Identifier(Procurements.SCHEMA),
                        sql.Identifier(Procurements.TABLE),
                        sql.Identifier(category)
                    )

                    cur.execute(query, (f"%{value}%",))

                    rows = cur.fetchall()

                    procurements = []
                    column_names = [desc[0] for desc in cur.description]
                    for row in rows:
                        procurements.append(dict(zip(column_names, row)))

                    return procurements
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error searching for procurement: {e}")
            return []    

    @staticmethod
    def update_version(**procurement_version) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor as cur:
                    columns = procurement_version.keys()
                    values = [procurement_version[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.versions ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Procurements.SCHEMA),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    procurement_id = cur.fetchone()[0]
                    conn.commit()
                    return procurement_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating procurement: {e}")
            conn.rollback()
            return None
        
    @staticmethod
    def update(procurement_id:int, **procurement_update) -> bool:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = procurement_update.keys()
                    values = [procurement_update[column] for column in columns]
                    values.append(procurement_id)

                    query = sql.SQL("""
                        UPDATE {}.{}
                        SET {}, updated_at = NOW()
                        WHERE id = %s
                        RETURNING *;
                    """).format(
                        sql.Identifier(Procurements.SCHEMA),
                        sql.Identifier(Procurements.TABLE),
                        sql.SQL(', ').join(sql.SQL("{} = {}").join(
                            map(sql.Identifier(column), sql.Placeholder(column)) for column in columns
                        ))
                    )

                    cur.execute(query, values)

                    updated_procurement = cur.fetchone()
                    conn.commit()

                    if updated_procurement:
                        print(f"Project with ID {procurement_id} updated successfully.")
                        print("Updated procurement:", updated_procurement)
                        return True
                    else:
                        print(f"No procurement found with ID {procurement_id}.")
                        return False
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error updating procurement {procurement_id}: {e}")
            conn.rollback()
            return False
    
    @staticmethod
    def delete(procurement_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    procurement = Procurements.read(procurement_id)
                    if not procurement:
                        print(f"Procurement with ID {procurement_id} not found.")
                        return {}

                    query = sql.SQL("""
                        DELETE FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Procurements.SCHEMA),
                        sql.Identifier(Procurements.TABLE)
                    )

                    cur.execute(query, (procurement_id,))

                    conn.commit()

                    print(f"Procurement with ID {procurement_id} deleted successfully.")
                    return procurement  
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error deleting procurement {procurement_id}: {e}")
            return {}


if __name__ == "__main__":
    pass
