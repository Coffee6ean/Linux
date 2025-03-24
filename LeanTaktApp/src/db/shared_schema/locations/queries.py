import psycopg
from psycopg import sql

import sys
sys.path.append('../')
from LeanTaktApp.src.db.utils.load_db import load_config

class Locations:

    SCHEMA = "shared_schema"
    TABLE = "locations"

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

                    cur.execute(query, (Locations.SCHEMA, Locations.TABLE))

                    available_columns = [row[0] for row in cur.fetchall()]
                    return available_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving location columns: {e}")
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

                    cur.execute(query, (Locations.SCHEMA, Locations.TABLE))

                    nullable_columns = [row[0] for row in cur.fetchall()]
                    return nullable_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving nullable columns: {e}")
            return []

    @staticmethod
    def create(**location:dict) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = location.keys()
                    values = [location[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.{} ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Locations.SCHEMA),
                        sql.Identifier(Locations.TABLE),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    location_id = cur.fetchone()[0]
                    conn.commit()
                    return location_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating location: {e}")
            conn.rollback()
            return None

    @staticmethod
    def read(location_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Locations.SCHEMA),
                        sql.Identifier(Locations.TABLE)
                    )

                    cur.execute(query, (location_id,))

                    row = cur.fetchone()

                    if row:
                        column_names = [desc[0] for desc in cur.description]
                        location = dict(zip(column_names, row))
                        return location
                    else:
                        return {}
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error reading location: {e}")
            return {}

    @staticmethod
    def read_all() -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT * FROM {}.{};").format(
                        sql.Identifier(Locations.SCHEMA),
                        sql.Identifier(Locations.TABLE)
                    )

                    cur.execute(query)
                    return cur.fetchall()
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Locations.SCHEMA}.{Locations.TABLE}: {e}")
            return []

    @staticmethod
    def read_all_from_category(value:str|int, category:str) -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    # Step 1: Get non-nullable columns
                    non_nullable_columns = Locations.get_non_nullable_columns()

                    if not non_nullable_columns:
                        print(f"No non-nullable columns found for table {Locations.SCHEMA}.{Locations.TABLE}.")
                        return []

                    # Step 2: Construct the SELECT clause for non-nullable columns
                    select_clause = sql.SQL(', ').join(map(sql.Identifier, non_nullable_columns))

                    # Step 3: Determine the column type
                    column_type_query = sql.SQL("""
                        SELECT data_type
                        FROM information_schema.columns
                        WHERE table_schema = %s AND table_name = %s AND column_name = %s;
                    """)
                    cur.execute(column_type_query, (Locations.SCHEMA, Locations.TABLE, category))
                    column_type = cur.fetchone()

                    if not column_type:
                        raise ValueError(f"Column '{category}' does not exist in table {Locations.SCHEMA}.{Locations.TABLE}.")

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
                            sql.Identifier(Locations.SCHEMA),
                            sql.Identifier(Locations.TABLE),
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
                            sql.Identifier(Locations.SCHEMA),
                            sql.Identifier(Locations.TABLE),
                            sql.Identifier(category)
                        )
                        value = f"%{value}%"

                    # Step 5: Execute the query
                    cur.execute(query, (value,))

                    # Step 6: Fetch all rows
                    rows = cur.fetchall()

                    # Step 7: Return the rows with non-nullable columns
                    return rows
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Locations.SCHEMA}.{Locations.TABLE}: {e}")
            return []

    @staticmethod
    def fetch_and_print_data() -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    non_nullable_columns = Locations.get_non_nullable_columns()

                    if not non_nullable_columns:
                        print(f"No non-nullable columns found for table {Locations.SCHEMA}.{Locations.TABLE}.")
                        return []

                    select_clause = sql.SQL(', ').join(map(sql.Identifier, non_nullable_columns))
                    query = sql.SQL("SELECT {} FROM {}.{};").format(
                        select_clause,
                        sql.Identifier(Locations.SCHEMA),
                        sql.Identifier(Locations.TABLE)
                    )

                    cur.execute(query)
                    non_nullable_rows = cur.fetchall()

                    non_nullable_data = [dict(zip(non_nullable_columns, row)) for row in non_nullable_rows]
                    return non_nullable_data
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from table {Locations.SCHEMA}.{Locations.TABLE}: {e}")
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
                        sql.Identifier(Locations.SCHEMA),
                        sql.Identifier(Locations.TABLE),
                        sql.Identifier(category)
                    )

                    cur.execute(query, (f"%{value}%",))

                    rows = cur.fetchall()

                    locations = []
                    column_names = [desc[0] for desc in cur.description]
                    for row in rows:
                        locations.append(dict(zip(column_names, row)))

                    return locations
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error searching for location: {e}")
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
                        sql.Identifier(Locations.SCHEMA),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    location_id = cur.fetchone()[0]
                    conn.commit()
                    return location_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating location: {e}")
            conn.rollback()
            return None
        
    @staticmethod
    def update(location_id:int, **location_update) -> bool:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = location_update.keys()
                    values = [location_update[column] for column in columns]
                    values.append(location_id)

                    query = sql.SQL("""
                        UPDATE {}.{}
                        SET {}, updated_at = NOW()
                        WHERE id = %s
                        RETURNING *;
                    """).format(
                        sql.Identifier(Locations.SCHEMA),
                        sql.Identifier(Locations.TABLE),
                        sql.SQL(', ').join(sql.SQL("{} = {}").join(
                            map(sql.Identifier(column), sql.Placeholder(column)) for column in columns
                        ))
                    )

                    cur.execute(query, values)

                    updated_location = cur.fetchone()
                    conn.commit()

                    if updated_location:
                        print(f"Location with ID {location_id} updated successfully.")
                        print("Updated location:", updated_location)
                        return True
                    else:
                        print(f"No location found with ID {location_id}.")
                        return False
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error updating location {location_id}: {e}")
            conn.rollback()
            return False
    
    @staticmethod
    def delete(location_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    location = Locations.read(location_id)
                    if not location:
                        print(f"Location with ID {location_id} not found.")
                        return {}

                    query = sql.SQL("""
                        DELETE FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Locations.SCHEMA),
                        sql.Identifier(Locations.TABLE)
                    )

                    cur.execute(query, (location_id,))

                    conn.commit()

                    print(f"Location with ID {location_id} deleted successfully.")
                    return location  
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error deleting location {location_id}: {e}")
            return {}


if __name__ == "__main__":
    pass
