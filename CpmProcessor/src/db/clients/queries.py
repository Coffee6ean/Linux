import psycopg
from psycopg import sql

import sys
sys.path.append('../')
from CpmProcessor.src.db.utils.load_db import load_config

class Clients:

    SCHEMA = "cpm_schema"
    TABLE = "clients"

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_column_names():
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT COLUMN_NAME
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;
                    """)

                    cur.execute(query, (Clients.SCHEMA, Clients.TABLE))

                    available_columns = [row[0] for row in cur.fetchall()]
                    return available_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving project columns: {e}")
            return []

    @staticmethod
    def create(**client:dict) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = client.keys()
                    values = [client[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.{} ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Clients.SCHEMA),
                        sql.Identifier(Clients.TABLE),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    client_id = cur.fetchone()[0]
                    conn.commit()
                    return client_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating client: {e}")
            conn.rollback()
            return None

    @staticmethod
    def read(client_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Clients.SCHEMA),
                        sql.Identifier(Clients.TABLE)
                    )

                    cur.execute(query, (client_id,))

                    row = cur.fetchone()

                    if row:
                        column_names = [desc[0] for desc in cur.description]
                        client = dict(zip(column_names, row))
                        return client
                    else:
                        return {}
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error reading client: {e}")
            return {}

    @staticmethod
    def read_all() -> list|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT * FROM {}.{};").format(
                        sql.Identifier(Clients.SCHEMA),
                        sql.Identifier(Clients.TABLE)
                    )

                    cur.execute(query)
                    return cur.fetchall()
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Clients.SCHEMA}.{Clients.TABLE}: {e}")
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
                        sql.Identifier(Clients.SCHEMA),
                        sql.Identifier(Clients.TABLE),
                        sql.Identifier(category)
                    )

                    cur.execute(query, (f"%{value}%",))

                    rows = cur.fetchall()

                    clients = []
                    column_names = [desc[0] for desc in cur.description]
                    for row in rows:
                        clients.append(dict(zip(column_names, row)))

                    return clients
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error searching for client: {e}")
            return []    

    @staticmethod
    def update_version(**client_version) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor as cur:
                    columns = client_version.keys()
                    values = [client_version[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.versions ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Clients.SCHEMA),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    client_id = cur.fetchone()[0]
                    conn.commit()
                    return client_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating client: {e}")
            conn.rollback()
            return None
        
    @staticmethod
    def update(client_id:int, **client_update) -> bool:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = client_update.keys()
                    values = [client_update[column] for column in columns]
                    values.append(client_id)

                    query = sql.SQL("""
                        UPDATE {}.{}
                        SET {}, updated_at = NOW()
                        WHERE id = %s
                        RETURNING *;
                    """).format(
                        sql.Identifier(Clients.SCHEMA),
                        sql.Identifier(Clients.TABLE),
                        sql.SQL(', ').join(sql.SQL("{} = {}").join(
                            map(sql.Identifier(column), sql.Placeholder(column)) for column in columns
                        ))
                    )

                    cur.execute(query, values)

                    updated_client = cur.fetchone()
                    conn.commit()

                    if updated_client:
                        print(f"Client with ID {client_id} updated successfully.")
                        print("Updated client:", updated_client)
                        return True
                    else:
                        print(f"No client found with ID {client_id}.")
                        return False
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error updating client {client_id}: {e}")
            conn.rollback()
            return False
    
    @staticmethod
    def delete(client_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    client = Clients.read(client_id)
                    if not client:
                        print(f"Client with ID {client_id} not found.")
                        return {}

                    query = sql.SQL("""
                        DELETE FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Clients.SCHEMA),
                        sql.Identifier(Clients.TABLE)
                    )

                    cur.execute(query, (client_id,))

                    conn.commit()

                    print(f"Client with ID {client_id} deleted successfully.")
                    return client  
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error deleting client {client_id}: {e}")
            return {}


if __name__ == "__main__":
    pass
