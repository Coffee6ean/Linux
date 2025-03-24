import psycopg
from psycopg import sql

import sys
sys.path.append('../')
from LeanTaktApp.src.db.utils.load_db import load_config

class Colors:

    SCHEMA = "shared_schema"
    TABLE = "colors"

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

                    cur.execute(query, (Colors.SCHEMA, Colors.TABLE))

                    available_columns = [row[0] for row in cur.fetchall()]
                    return available_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving table columns: {e}")
            return []

    @staticmethod
    def get_non_nullable_columns() -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT COLUMN_NAME
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND IS_NULLABLE = 'NO';
                    """)

                    cur.execute(query, (Colors.SCHEMA, Colors.TABLE))

                    nullable_columns = [row[0] for row in cur.fetchall()]
                    return nullable_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving nullable columns: {e}")
            return []

    @staticmethod
    def create(**color:dict) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = color.keys()
                    values = [color[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.{} ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Colors.SCHEMA),
                        sql.Identifier(Colors.TABLE),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    color_id = cur.fetchone()[0]
                    conn.commit()
                    return color_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating color: {e}")
            conn.rollback()
            return None

    @staticmethod
    def read(color_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Colors.SCHEMA),
                        sql.Identifier(Colors.TABLE)
                    )

                    cur.execute(query, (color_id,))

                    row = cur.fetchone()

                    if row:
                        column_names = [desc[0] for desc in cur.description]
                        color = dict(zip(column_names, row))
                        return color
                    else:
                        return {}
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error reading color: {e}")
            return {}

    @staticmethod
    def read_all() -> list|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT * FROM {}.{};").format(
                        sql.Identifier(Colors.SCHEMA),
                        sql.Identifier(Colors.TABLE)
                    )

                    cur.execute(query)
                    return cur.fetchall()
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Colors.SCHEMA}.{Colors.TABLE}: {e}")
            return None

    @staticmethod
    def read_all_from_category(value, category:str) -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    # Step 1: Get non-nullable columns
                    non_nullable_columns = Colors.get_non_nullable_columns()

                    if not non_nullable_columns:
                        print(f"No non-nullable columns found for table {Colors.SCHEMA}.{Colors.TABLE}.")
                        return []

                    # Step 2: Construct the SELECT clause for non-nullable columns
                    select_clause = sql.SQL(', ').join(map(sql.Identifier, non_nullable_columns))

                    # Step 3: Determine the column type
                    column_type_query = sql.SQL("""
                        SELECT data_type
                        FROM information_schema.columns
                        WHERE table_schema = %s AND table_name = %s AND column_name = %s;
                    """)
                    cur.execute(column_type_query, (Colors.SCHEMA, Colors.TABLE, category))
                    column_type = cur.fetchone()

                    if not column_type:
                        raise ValueError(f"Column '{category}' does not exist in table {Colors.SCHEMA}.{Colors.TABLE}.")

                    column_type = column_type[0]

                    # Step 4: Construct the query based on the column type
                    if column_type in ('integer', 'bigint', 'smallint', 'numeric'):
                        # For integer columns, use exact matching
                        query = sql.SQL("""
                            SELECT {}
                            FROM {}.{}
                            WHERE {} = %s;
                        """).format(
                            select_clause,
                            sql.Identifier(Colors.SCHEMA),
                            sql.Identifier(Colors.TABLE),
                            sql.Identifier(category)
                        )
                    else:
                        # For text/string columns, use ILIKE with wildcards
                        query = sql.SQL("""
                            SELECT {}
                            FROM {}.{}
                            WHERE {} ILIKE %s;
                        """).format(
                            select_clause,
                            sql.Identifier(Colors.SCHEMA),
                            sql.Identifier(Colors.TABLE),
                            sql.Identifier(category)
                        )
                        value = f"%{value}%"

                    # Step 5: Execute the query
                    cur.execute(query, (value,))

                    # Step 6: Fetch all rows
                    rows = cur.fetchall()
                    proc_rows = [dict(zip(non_nullable_columns, row)) for row in rows]

                    # Step 7: Return the rows with non-nullable columns
                    return proc_rows
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Colors.SCHEMA}.{Colors.TABLE}: {e}")
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
                        sql.Identifier(Colors.SCHEMA),
                        sql.Identifier(Colors.TABLE),
                        sql.Identifier(category)
                    )

                    cur.execute(query, (f"%{value}%",))

                    rows = cur.fetchall()

                    colors = []
                    column_names = [desc[0] for desc in cur.description]
                    for row in rows:
                        colors.append(dict(zip(column_names, row)))

                    return colors
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error searching for color: {e}")
            return []    

    @staticmethod
    def update_version(**color_version) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor as cur:
                    columns = color_version.keys()
                    values = [color_version[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.versions ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Colors.SCHEMA),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    color_id = cur.fetchone()[0]
                    conn.commit()
                    return color_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating color: {e}")
            conn.rollback()
            return None
        
    @staticmethod
    def update(color_id:int, **color_update) -> bool:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = color_update.keys()
                    values = [color_update[column] for column in columns]
                    values.append(color_id)

                    query = sql.SQL("""
                        UPDATE {}.{}
                        SET {}, updated_at = NOW()
                        WHERE id = %s
                        RETURNING *;
                    """).format(
                        sql.Identifier(Colors.SCHEMA),
                        sql.Identifier(Colors.TABLE),
                        sql.SQL(', ').join(sql.SQL("{} = {}").join(
                            map(sql.Identifier(column), sql.Placeholder(column)) for column in columns
                        ))
                    )

                    cur.execute(query, values)

                    updated_activity = cur.fetchone()
                    conn.commit()

                    if updated_activity:
                        print(f"Color with ID {color_id} updated successfully.")
                        print("Updated color:", updated_activity)
                        return True
                    else:
                        print(f"No color found with ID {color_id}.")
                        return False
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error updating color {color_id}: {e}")
            conn.rollback()
            return False
    
    @staticmethod
    def delete(color_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    color = Colors.read(color_id)
                    if not color:
                        print(f"Color with ID {color_id} not found.")
                        return {}

                    query = sql.SQL("""
                        DELETE FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Colors.SCHEMA),
                        sql.Identifier(Colors.TABLE)
                    )

                    cur.execute(query, (color_id,))

                    conn.commit()

                    print(f"Color with ID {color_id} deleted successfully.")
                    return color  
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error deleting color {color_id}: {e}")
            return {}


if __name__ == "__main__":
    pass
