import psycopg
from psycopg import sql

import sys
sys.path.append('../')
from CpmProcessor.src.db.utils.load_db import load_config

class Activities:

    SCHEMA = "cpm_schema"
    TABLE = "activities"

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

                    cur.execute(query, (Activities.SCHEMA, Activities.TABLE))

                    available_columns = [row[0] for row in cur.fetchall()]
                    return available_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving project columns: {e}")
            return []

    @staticmethod
    def create(**activity:dict) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = activity.keys()
                    values = [activity[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.{} ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Activities.SCHEMA),
                        sql.Identifier(Activities.TABLE),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    activity_id = cur.fetchone()[0]
                    conn.commit()
                    return activity_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating activity: {e}")
            conn.rollback()
            return None

    @staticmethod
    def read(activity_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Activities.SCHEMA),
                        sql.Identifier(Activities.TABLE)
                    )

                    cur.execute(query, (activity_id,))

                    row = cur.fetchone()

                    if row:
                        column_names = [desc[0] for desc in cur.description]
                        activity = dict(zip(column_names, row))
                        return activity
                    else:
                        return {}
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error reading activity: {e}")
            return {}

    @staticmethod
    def read_all() -> list|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT * FROM {}.{};").format(
                        sql.Identifier(Activities.SCHEMA),
                        sql.Identifier(Activities.TABLE)
                    )

                    cur.execute(query)
                    return cur.fetchall()
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Activities.SCHEMA}.{Activities.TABLE}: {e}")
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
                        sql.Identifier(Activities.SCHEMA),
                        sql.Identifier(Activities.TABLE),
                        sql.Identifier(category)
                    )

                    cur.execute(query, (f"%{value}%",))

                    rows = cur.fetchall()

                    activities = []
                    column_names = [desc[0] for desc in cur.description]
                    for row in rows:
                        activities.append(dict(zip(column_names, row)))

                    return activities
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error searching for activity: {e}")
            return []    

    @staticmethod
    def update_version(**activity_version) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor as cur:
                    columns = activity_version.keys()
                    values = [activity_version[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.versions ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Activities.SCHEMA),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    activity_id = cur.fetchone()[0]
                    conn.commit()
                    return activity_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating activity: {e}")
            conn.rollback()
            return None
        
    @staticmethod
    def update(activity_id:int, **activity_update) -> bool:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = activity_update.keys()
                    values = [activity_update[column] for column in columns]
                    values.append(activity_id)

                    query = sql.SQL("""
                        UPDATE {}.{}
                        SET {}, updated_at = NOW()
                        WHERE id = %s
                        RETURNING *;
                    """).format(
                        sql.Identifier(Activities.SCHEMA),
                        sql.Identifier(Activities.TABLE),
                        sql.SQL(', ').join(sql.SQL("{} = {}").join(
                            map(sql.Identifier(column), sql.Placeholder(column)) for column in columns
                        ))
                    )

                    cur.execute(query, values)

                    updated_activity = cur.fetchone()
                    conn.commit()

                    if updated_activity:
                        print(f"Project with ID {activity_id} updated successfully.")
                        print("Updated activity:", updated_activity)
                        return True
                    else:
                        print(f"No activity found with ID {activity_id}.")
                        return False
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error updating activity {activity_id}: {e}")
            conn.rollback()
            return False
    
    @staticmethod
    def delete(activity_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    activity = Activities.read(activity_id)
                    if not activity:
                        print(f"Activity with ID {activity_id} not found.")
                        return {}

                    query = sql.SQL("""
                        DELETE FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Activities.SCHEMA),
                        sql.Identifier(Activities.TABLE)
                    )

                    cur.execute(query, (activity_id,))

                    conn.commit()

                    print(f"Activity with ID {activity_id} deleted successfully.")
                    return activity  
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error deleting activity {activity_id}: {e}")
            return {}


if __name__ == "__main__":
    pass
