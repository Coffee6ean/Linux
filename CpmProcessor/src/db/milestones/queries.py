import psycopg
from psycopg import sql

import sys
sys.path.append('../')
from CpmProcessor.src.db.utils.load_db import load_config

class Milestones:

    SCHEMA = "cpm_schema"
    TABLE = "milestones"

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

                    cur.execute(query, (Milestones.SCHEMA, Milestones.TABLE))

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

                    cur.execute(query, (Milestones.SCHEMA, Milestones.TABLE))

                    nullable_columns = [row[0] for row in cur.fetchall()]
                    return nullable_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving nullable columns: {e}")
            return []

    @staticmethod
    def create(**milestone:dict) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = milestone.keys()
                    values = [milestone[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.{} ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Milestones.SCHEMA),
                        sql.Identifier(Milestones.TABLE),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    milestone_id = cur.fetchone()[0]
                    conn.commit()
                    return milestone_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating milestone: {e}")
            conn.rollback()
            return None

    @staticmethod
    def read(milestone_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Milestones.SCHEMA),
                        sql.Identifier(Milestones.TABLE)
                    )

                    cur.execute(query, (milestone_id,))

                    row = cur.fetchone()

                    if row:
                        column_names = [desc[0] for desc in cur.description]
                        milestone = dict(zip(column_names, row))
                        return milestone
                    else:
                        return {}
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error reading milestone: {e}")
            return {}

    @staticmethod
    def read_all() -> list|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT * FROM {}.{};").format(
                        sql.Identifier(Milestones.SCHEMA),
                        sql.Identifier(Milestones.TABLE)
                    )

                    cur.execute(query)
                    return cur.fetchall()
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Milestones.SCHEMA}.{Milestones.TABLE}: {e}")
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
                        sql.Identifier(Milestones.SCHEMA),
                        sql.Identifier(Milestones.TABLE),
                        sql.Identifier(category)
                    )

                    cur.execute(query, (f"%{value}%",))

                    rows = cur.fetchall()

                    milestones = []
                    column_names = [desc[0] for desc in cur.description]
                    for row in rows:
                        milestones.append(dict(zip(column_names, row)))

                    return milestones
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error searching for milestone: {e}")
            return []    

    @staticmethod
    def update_version(**milestone_version) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor as cur:
                    columns = milestone_version.keys()
                    values = [milestone_version[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.versions ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Milestones.SCHEMA),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    milestone_id = cur.fetchone()[0]
                    conn.commit()
                    return milestone_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating milestone: {e}")
            conn.rollback()
            return None
        
    @staticmethod
    def update(milestone_id:int, **milestone_update) -> bool:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = milestone_update.keys()
                    values = [milestone_update[column] for column in columns]
                    values.append(milestone_id)

                    query = sql.SQL("""
                        UPDATE {}.{}
                        SET {}, updated_at = NOW()
                        WHERE id = %s
                        RETURNING *;
                    """).format(
                        sql.Identifier(Milestones.SCHEMA),
                        sql.Identifier(Milestones.TABLE),
                        sql.SQL(', ').join(sql.SQL("{} = {}").join(
                            map(sql.Identifier(column), sql.Placeholder(column)) for column in columns
                        ))
                    )

                    cur.execute(query, values)

                    updated_milestone = cur.fetchone()
                    conn.commit()

                    if updated_milestone:
                        print(f"Project with ID {milestone_id} updated successfully.")
                        print("Updated milestone:", updated_milestone)
                        return True
                    else:
                        print(f"No milestone found with ID {milestone_id}.")
                        return False
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error updating milestone {milestone_id}: {e}")
            conn.rollback()
            return False
    
    @staticmethod
    def delete(milestone_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    milestone = Milestones.read(milestone_id)
                    if not milestone:
                        print(f"Activity with ID {milestone_id} not found.")
                        return {}

                    query = sql.SQL("""
                        DELETE FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Milestones.SCHEMA),
                        sql.Identifier(Milestones.TABLE)
                    )

                    cur.execute(query, (milestone_id,))

                    conn.commit()

                    print(f"Activity with ID {milestone_id} deleted successfully.")
                    return milestone  
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error deleting milestone {milestone_id}: {e}")
            return {}


if __name__ == "__main__":
    pass
