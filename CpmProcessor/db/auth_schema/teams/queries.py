import psycopg
from psycopg import sql

import sys
sys.path.append('../')
from LeanTaktApp.src.db.utils.load_db import load_config

class Teams:

    SCHEMA = "auth_schema"
    TABLE = "teams"

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_column_names(table_name:str=TABLE) -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT COLUMN_NAME
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;
                    """)

                    cur.execute(query, (Teams.SCHEMA, table_name))

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

                    cur.execute(query, (Teams.SCHEMA, Teams.TABLE))

                    nullable_columns = [row[0] for row in cur.fetchall()]
                    return nullable_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving nullable columns: {e}")
            return []

    @staticmethod
    def create(**team:dict) -> int | None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = team.keys()
                    values = [team[column] for column in columns]

                    placeholders = sql.SQL(', ').join([sql.Placeholder()] * len(values))

                    query = sql.SQL("""
                        INSERT INTO {}.{} ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Teams.SCHEMA),
                        sql.Identifier(Teams.TABLE),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        placeholders
                    )

                    cur.execute(query, values)
                    team_id = cur.fetchone()[0]

                    conn.commit()
                    return team_id
                
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating team: {e}")
            if conn:  # Ensure conn is defined before rolling back
                conn.rollback()
            return None

    @staticmethod
    def read(team_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Teams.SCHEMA),
                        sql.Identifier(Teams.TABLE)
                    )

                    cur.execute(query, (team_id,))

                    row = cur.fetchone()

                    if row:
                        column_names = [desc[0] for desc in cur.description]
                        team = dict(zip(column_names, row))
                        return team
                    else:
                        return {}
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error reading team: {e}")
            return {}

    @staticmethod
    def read_all() -> list|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT * FROM {}.{};").format(
                        sql.Identifier(Teams.SCHEMA),
                        sql.Identifier(Teams.TABLE)
                    )

                    cur.execute(query)
                    return cur.fetchall()
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Teams.SCHEMA}.{Teams.TABLE}: {e}")
            return None

    @staticmethod
    def read_all_from_category(value, category:str) -> list:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    # Step 1: Get non-nullable columns
                    non_nullable_columns = Teams.get_non_nullable_columns()

                    if not non_nullable_columns:
                        print(f"No non-nullable columns found for table {Teams.SCHEMA}.{Teams.TABLE}.")
                        return []

                    # Step 2: Construct the SELECT clause for non-nullable columns
                    select_clause = sql.SQL(', ').join(map(sql.Identifier, non_nullable_columns))

                    # Step 3: Determine the column type
                    column_type_query = sql.SQL("""
                        SELECT data_type
                        FROM information_schema.columns
                        WHERE table_schema = %s AND table_name = %s AND column_name = %s;
                    """)
                    cur.execute(column_type_query, (Teams.SCHEMA, Teams.TABLE, category))
                    column_type = cur.fetchone()

                    if not column_type:
                        raise ValueError(f"Column '{category}' does not exist in table {Teams.SCHEMA}.{Teams.TABLE}.")

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
                            sql.Identifier(Teams.SCHEMA),
                            sql.Identifier(Teams.TABLE),
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
                            sql.Identifier(Teams.SCHEMA),
                            sql.Identifier(Teams.TABLE),
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
            print(f"Error fetching data from {Teams.SCHEMA}.{Teams.TABLE}: {e}")
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
                        sql.Identifier(Teams.SCHEMA),
                        sql.Identifier(Teams.TABLE),
                        sql.Identifier(category)
                    )

                    cur.execute(query, (f"%{value}%",))

                    rows = cur.fetchall()

                    teams = []
                    column_names = [desc[0] for desc in cur.description]
                    for row in rows:
                        teams.append(dict(zip(column_names, row)))

                    return teams
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error searching for team: {e}")
            return []    

    @staticmethod
    def update(team_id: int, **team_update) -> bool:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    # Prepare the SET clause
                    columns = team_update.keys()
                    set_clause = sql.SQL(', ').join(
                        sql.SQL("{} = %s").format(sql.Identifier(col)) for col in columns
                    )

                    # Prepare the values for the SET clause and the WHERE clause
                    values = [team_update[col] for col in columns]
                    values.append(team_id)  # Add team_id for the WHERE clause

                    # Construct the query
                    query = sql.SQL("""
                        UPDATE {}.{}
                        SET {}, updated_at = NOW()
                        WHERE id = %s
                        RETURNING *;
                    """).format(
                        sql.Identifier(Teams.SCHEMA),
                        sql.Identifier(Teams.TABLE),
                        set_clause
                    )

                    # Execute the query
                    cur.execute(query, values)

                    # Fetch the updated row
                    updated_team = cur.fetchone()
                    conn.commit()

                    if updated_team:
                        print(f"Team with ID {team_id} updated successfully.")
                        print("Updated team:", updated_team)
                        return True
                    else:
                        print(f"No team found with ID {team_id}.")
                        return False

        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error updating team {team_id}: {e}")
            if conn:
                conn.rollback()
            return False
    
    @staticmethod
    def delete(team_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    team = Teams.read(team_id)
                    if not team:
                        print(f"Team with ID {team_id} not found.")
                        return {}

                    query = sql.SQL("""
                        DELETE FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Teams.SCHEMA),
                        sql.Identifier(Teams.TABLE)
                    )

                    cur.execute(query, (team_id,))

                    conn.commit()

                    print(f"Team with ID {team_id} deleted successfully.")
                    return team  
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error deleting team {team_id}: {e}")
            return {}


if __name__ == "__main__":
    pass
