import psycopg
from psycopg import sql

import sys
sys.path.append('../')
from CpmProcessor.src.db.utils.load_db import load_config

class Tags:

    SCHEMA = "cpm_schema"
    TABLE = "tags"

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

                    cur.execute(query, (Tags.SCHEMA, Tags.TABLE))

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

                    cur.execute(query, (Tags.SCHEMA, Tags.TABLE))

                    nullable_columns = [row[0] for row in cur.fetchall()]
                    return nullable_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving nullable columns: {e}")
            return []

    @staticmethod
    def create(**tag:dict) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = tag.keys()
                    values = [tag[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.{} ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Tags.SCHEMA),
                        sql.Identifier(Tags.TABLE),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    tag_id = cur.fetchone()[0]
                    conn.commit()
                    return tag_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating tag: {e}")
            conn.rollback()
            return None

    @staticmethod
    def read(tag_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Tags.SCHEMA),
                        sql.Identifier(Tags.TABLE)
                    )

                    cur.execute(query, (tag_id,))

                    row = cur.fetchone()

                    if row:
                        column_names = [desc[0] for desc in cur.description]
                        tag = dict(zip(column_names, row))
                        return tag
                    else:
                        return {}
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error reading tag: {e}")
            return {}

    @staticmethod
    def read_all() -> list|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT * FROM {}.{};").format(
                        sql.Identifier(Tags.SCHEMA),
                        sql.Identifier(Tags.TABLE)
                    )

                    cur.execute(query)
                    return cur.fetchall()
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Tags.SCHEMA}.{Tags.TABLE}: {e}")
            return None

    @staticmethod
    def read_all_from_category(value, category: str) -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    # Step 1: Get non-nullable columns
                    non_nullable_columns = Tags.get_non_nullable_columns()

                    if not non_nullable_columns:
                        print(f"No non-nullable columns found for table {Tags.SCHEMA}.{Tags.TABLE}.")
                        return []

                    # Step 2: Construct the SELECT clause for non-nullable columns
                    select_clause = sql.SQL(', ').join(map(sql.Identifier, non_nullable_columns))

                    # Step 3: Determine the column type
                    column_type_query = sql.SQL("""
                        SELECT data_type
                        FROM information_schema.columns
                        WHERE table_schema = %s AND table_name = %s AND column_name = %s;
                    """)
                    cur.execute(column_type_query, (Tags.SCHEMA, Tags.TABLE, category))
                    column_type = cur.fetchone()

                    if not column_type:
                        raise ValueError(f"Column '{category}' does not exist in table {Tags.SCHEMA}.{Tags.TABLE}.")

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
                            sql.Identifier(Tags.SCHEMA),
                            sql.Identifier(Tags.TABLE),
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
                            sql.Identifier(Tags.SCHEMA),
                            sql.Identifier(Tags.TABLE),
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
            print(f"Error fetching data from {Tags.SCHEMA}.{Tags.TABLE}: {e}")
            return []

    @staticmethod
    def fetch_and_print_data() -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    non_nullable_columns = Tags.get_non_nullable_columns()

                    if not non_nullable_columns:
                        print(f"No non-nullable columns found for table {Tags.SCHEMA}.{Tags.TABLE}.")
                        return []

                    select_clause = sql.SQL(', ').join(map(sql.Identifier, non_nullable_columns))
                    query = sql.SQL("SELECT {} FROM {}.{};").format(
                        select_clause,
                        sql.Identifier(Tags.SCHEMA),
                        sql.Identifier(Tags.TABLE)
                    )

                    cur.execute(query)
                    non_nullable_rows = cur.fetchall()

                    non_nullable_data = [dict(zip(non_nullable_columns, row)) for row in non_nullable_rows]
                    return non_nullable_data
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from table {Tags.SCHEMA}.{Tags.TABLE}: {e}")
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
                        sql.Identifier(Tags.SCHEMA),
                        sql.Identifier(Tags.TABLE),
                        sql.Identifier(category)
                    )

                    cur.execute(query, (f"%{value}%",))

                    rows = cur.fetchall()

                    tags = []
                    column_names = [desc[0] for desc in cur.description]
                    for row in rows:
                        tags.append(dict(zip(column_names, row)))

                    return tags
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error searching for tag: {e}")
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
                        sql.Identifier(Tags.SCHEMA),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    tag_id = cur.fetchone()[0]
                    conn.commit()
                    return tag_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating tag: {e}")
            conn.rollback()
            return None
        
    @staticmethod
    def update(tag_id:int, **tag_update) -> bool:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = tag_update.keys()
                    values = [tag_update[column] for column in columns]
                    values.append(tag_id)

                    query = sql.SQL("""
                        UPDATE {}.{}
                        SET {}, updated_at = NOW()
                        WHERE id = %s
                        RETURNING *;
                    """).format(
                        sql.Identifier(Tags.SCHEMA),
                        sql.Identifier(Tags.TABLE),
                        sql.SQL(', ').join(sql.SQL("{} = {}").join(
                            map(sql.Identifier(column), sql.Placeholder(column)) for column in columns
                        ))
                    )

                    cur.execute(query, values)

                    updated_tag = cur.fetchone()
                    conn.commit()

                    if updated_tag:
                        print(f"Tag with ID {tag_id} updated successfully.")
                        print("Updated tag:", updated_tag)
                        return True
                    else:
                        print(f"No tag found with ID {tag_id}.")
                        return False
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error updating tag {tag_id}: {e}")
            conn.rollback()
            return False
    
    @staticmethod
    def delete(tag_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    tag = Tags.read(tag_id)
                    if not tag:
                        print(f"Tag with ID {tag_id} not found.")
                        return {}

                    query = sql.SQL("""
                        DELETE FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Tags.SCHEMA),
                        sql.Identifier(Tags.TABLE)
                    )

                    cur.execute(query, (tag_id,))

                    conn.commit()

                    print(f"Tag with ID {tag_id} deleted successfully.")
                    return tag  
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error deleting tag {tag_id}: {e}")
            return {}


if __name__ == "__main__":
    pass
