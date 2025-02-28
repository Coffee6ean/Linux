import psycopg
from psycopg import sql

import sys
sys.path.append('../')
from CpmProcessor.src.db.utils.load_db import load_config

class Users:

    SCHEMA = "cpm_schema"
    TABLE = "users"

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

                    cur.execute(query, (Users.SCHEMA, Users.TABLE))

                    available_columns = [row[0] for row in cur.fetchall()]
                    return available_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving project columns: {e}")
            return []
    
    @staticmethod
    def create(**user:dict) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = user.keys()
                    values = [user[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.{} ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Users.SCHEMA),
                        sql.Identifier(Users.TABLE),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    user_id = cur.fetchone()[0]
                    conn.commit()
                    return user_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating user: {e}")
            conn.rollback()
            return None

    @staticmethod
    def read(user_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Users.SCHEMA),
                        sql.Identifier(Users.TABLE)
                    )

                    cur.execute(query, (user_id,))

                    row = cur.fetchone()

                    if row:
                        column_names = [desc[0] for desc in cur.description]
                        user = dict(zip(column_names, row))
                        return user
                    else:
                        return {}
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error reading user: {e}")
            return {}

    @staticmethod
    def read_all() -> list|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT * FROM {}.{};").format(
                        sql.Identifier(Users.SCHEMA),
                        sql.Identifier(Users.TABLE)
                    )

                    cur.execute(query)
                    return cur.fetchall()
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Users.SCHEMA}.{Users.TABLE}: {e}")
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
                        sql.Identifier(Users.SCHEMA),
                        sql.Identifier(Users.TABLE),
                        sql.Identifier(category)
                    )

                    cur.execute(query, (f"%{value}%",))

                    rows = cur.fetchall()

                    users = []
                    column_names = [desc[0] for desc in cur.description]
                    for row in rows:
                        users.append(dict(zip(column_names, row)))

                    return users
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error searching for user: {e}")
            return []    

    @staticmethod
    def update_version(**user_version:dict) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor as cur:
                    columns = user_version.keys()
                    values = [user_version[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.versions ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Users.SCHEMA),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    user_id = cur.fetchone()[0]
                    conn.commit()
                    return user_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating user: {e}")
            conn.rollback()
            return None
        
    @staticmethod
    def update(user_id:int, **user_update:dict) -> bool:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = user_update.keys()
                    values = [user_update[column] for column in columns]
                    values.append(user_id)

                    query = sql.SQL("""
                        UPDATE {}.{}
                        SET {}, updated_at = NOW()
                        WHERE id = %s
                        RETURNING *;
                    """).format(
                        sql.Identifier(Users.SCHEMA),
                        sql.Identifier(Users.TABLE),
                        sql.SQL(', ').join(sql.SQL("{} = {}").join(
                            map(sql.Identifier(column), sql.Placeholder(column)) for column in columns
                        ))
                    )

                    cur.execute(query, values)

                    updated_user = cur.fetchone()
                    conn.commit()

                    if updated_user:
                        print(f"User with ID {user_id} updated successfully.")
                        print("Updated user:", updated_user)
                        return True
                    else:
                        print(f"No user found with ID {user_id}.")
                        return False
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error updating user {user_id}: {e}")
            conn.rollback()
            return False
    
    @staticmethod
    def delete(user_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    user = Users.read(user_id)
                    if not user:
                        print(f"User with ID {user_id} not found.")
                        return {}

                    query = sql.SQL("""
                        DELETE FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Users.SCHEMA),
                        sql.Identifier(Users.TABLE)
                    )

                    cur.execute(query, (user_id,))

                    conn.commit()

                    print(f"User with ID {user_id} deleted successfully.")
                    return user  
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error deleting user {user_id}: {e}")
            return {}


if __name__ == "__main__":
    pass
