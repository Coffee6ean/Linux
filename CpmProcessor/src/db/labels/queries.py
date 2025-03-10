import psycopg
from psycopg import sql

import sys
sys.path.append('../')
from CpmProcessor.src.db.utils.load_db import load_config

class Labels:

    SCHEMA = "cpm_schema"
    TABLE = "labels"

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

                    cur.execute(query, (Labels.SCHEMA, Labels.TABLE))

                    available_columns = [row[0] for row in cur.fetchall()]
                    return available_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving label columns: {e}")
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

                    cur.execute(query, (Labels.SCHEMA, Labels.TABLE))

                    nullable_columns = [row[0] for row in cur.fetchall()]
                    return nullable_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving nullable columns: {e}")
            return []

    @staticmethod
    def create(**label:dict) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = label.keys()
                    values = [label[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.{} ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Labels.SCHEMA),
                        sql.Identifier(Labels.TABLE),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    label_id = cur.fetchone()[0]
                    conn.commit()
                    return label_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating label: {e}")
            conn.rollback()
            return None

    @staticmethod
    def read(label_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Labels.SCHEMA),
                        sql.Identifier(Labels.TABLE)
                    )

                    cur.execute(query, (label_id,))

                    row = cur.fetchone()

                    if row:
                        column_names = [desc[0] for desc in cur.description]
                        label = dict(zip(column_names, row))
                        return label
                    else:
                        return {}
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error reading label: {e}")
            return {}

    @staticmethod
    def read_all() -> list|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT * FROM {}.{};").format(
                        sql.Identifier(Labels.SCHEMA),
                        sql.Identifier(Labels.TABLE)
                    )

                    cur.execute(query)
                    return cur.fetchall()
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Labels.SCHEMA}.{Labels.TABLE}: {e}")
            return None

    @staticmethod
    def fetch_and_print_data() -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    non_nullable_columns = Labels.get_non_nullable_columns()

                    if not non_nullable_columns:
                        print(f"No non-nullable columns found for table {Labels.SCHEMA}.{Labels.TABLE}.")
                        return []

                    select_clause = sql.SQL(', ').join(map(sql.Identifier, non_nullable_columns))
                    query = sql.SQL("SELECT {} FROM {}.{};").format(
                        select_clause,
                        sql.Identifier(Labels.SCHEMA),
                        sql.Identifier(Labels.TABLE)
                    )

                    cur.execute(query)
                    non_nullable_rows = cur.fetchall()

                    non_nullable_data = [dict(zip(non_nullable_columns, row)) for row in non_nullable_rows]
                    return non_nullable_data
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from table {Labels.SCHEMA}.{Labels.TABLE}: {e}")
            return []

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
                        sql.Identifier(Labels.SCHEMA),
                        sql.Identifier(Labels.TABLE),
                        sql.Identifier(category)
                    )

                    cur.execute(query, (f"%{value}%",))

                    rows = cur.fetchall()

                    labels = []
                    column_names = [desc[0] for desc in cur.description]
                    for row in rows:
                        labels.append(dict(zip(column_names, row)))

                    return labels
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error searching for label: {e}")
            return []    

    @staticmethod
    def update_version(**label_version) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor as cur:
                    columns = label_version.keys()
                    values = [label_version[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.versions ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Labels.SCHEMA),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    label_id = cur.fetchone()[0]
                    conn.commit()
                    return label_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating label: {e}")
            conn.rollback()
            return None
        
    @staticmethod
    def update(label_id:int, **label_update) -> bool:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = label_update.keys()
                    values = [label_update[column] for column in columns]
                    values.append(label_id)

                    query = sql.SQL("""
                        UPDATE {}.{}
                        SET {}, updated_at = NOW()
                        WHERE id = %s
                        RETURNING *;
                    """).format(
                        sql.Identifier(Labels.SCHEMA),
                        sql.Identifier(Labels.TABLE),
                        sql.SQL(', ').join(sql.SQL("{} = {}").join(
                            map(sql.Identifier(column), sql.Placeholder(column)) for column in columns
                        ))
                    )

                    cur.execute(query, values)

                    updated_label = cur.fetchone()
                    conn.commit()

                    if updated_label:
                        print(f"Label with ID {label_id} updated successfully.")
                        print("Updated label:", updated_label)
                        return True
                    else:
                        print(f"No label found with ID {label_id}.")
                        return False
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error updating label {label_id}: {e}")
            conn.rollback()
            return False
    
    @staticmethod
    def delete(label_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    label = Labels.read(label_id)
                    if not label:
                        print(f"Label with ID {label_id} not found.")
                        return {}

                    query = sql.SQL("""
                        DELETE FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Labels.SCHEMA),
                        sql.Identifier(Labels.TABLE)
                    )

                    cur.execute(query, (label_id,))

                    conn.commit()

                    print(f"Label with ID {label_id} deleted successfully.")
                    return label  
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error deleting label {label_id}: {e}")
            return {}


if __name__ == "__main__":
    pass
