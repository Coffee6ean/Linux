import psycopg
from psycopg import sql

import sys
sys.path.append('../')
from CpmProcessor.src.db.utils.load_db import load_config

class Projects:

    SCHEMA = "cpm_schema"
    TABLE = "projects"

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

                    cur.execute(query, (Projects.SCHEMA, Projects.TABLE))

                    available_columns = [row[0] for row in cur.fetchall()]
                    return available_columns
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error retrieving project columns: {e}")
            return []

    @staticmethod
    def create(**project:dict) -> int|None:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = project.keys()
                    values = [project[column] for column in columns]

                    query = sql.SQL("""
                        INSERT INTO {}.{} ({})
                        VALUES ({})
                        RETURNING id;
                    """).format(
                        sql.Identifier(Projects.SCHEMA),
                        sql.Identifier(Projects.TABLE),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    project_id = cur.fetchone()[0]
                    conn.commit()
                    return project_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating project: {e}")
            conn.rollback()
            return None

    @staticmethod
    def read(project_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""
                        SELECT *
                        FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Projects.SCHEMA),
                        sql.Identifier(Projects.TABLE)
                    )

                    cur.execute(query, (project_id,))

                    row = cur.fetchone()

                    if row:
                        column_names = [desc[0] for desc in cur.description]
                        project = dict(zip(column_names, row))
                        return project
                    else:
                        return {}
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error reading project: {e}")
            return {}

    @staticmethod
    def read_all() -> list|None:
        try:
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("SELECT * FROM {}.{};").format(
                        sql.Identifier(Projects.SCHEMA),
                        sql.Identifier(Projects.TABLE)
                    )

                    cur.execute(query)
                    return cur.fetchall()
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error fetching data from {Projects.SCHEMA}.{Projects.TABLE}: {e}")
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
                        sql.Identifier(Projects.SCHEMA),
                        sql.Identifier(Projects.TABLE),
                        sql.Identifier(category)
                    )

                    cur.execute(query, (f"%{value}%",))

                    rows = cur.fetchall()

                    projects = []
                    column_names = [desc[0] for desc in cur.description]
                    for row in rows:
                        projects.append(dict(zip(column_names, row)))

                    return projects
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error searching for project: {e}")
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
                        sql.Identifier(Projects.SCHEMA),
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(map(sql.Placeholder, columns))
                    )

                    cur.execute(query, values)
                    project_id = cur.fetchone()[0]
                    conn.commit()
                    return project_id
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error creating project: {e}")
            conn.rollback()
            return None
        
    @staticmethod
    def update(project_id:int, **project_update) -> bool:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    columns = project_update.keys()
                    values = [project_update[column] for column in columns]
                    values.append(project_id)

                    query = sql.SQL("""
                        UPDATE {}.{}
                        SET {}, updated_at = NOW()
                        WHERE id = %s
                        RETURNING *;
                    """).format(
                        sql.Identifier(Projects.SCHEMA),
                        sql.Identifier(Projects.TABLE),
                        sql.SQL(', ').join(sql.SQL("{} = {}").join(
                            map(sql.Identifier(column), sql.Placeholder(column)) for column in columns
                        ))
                    )

                    cur.execute(query, values)

                    updated_project = cur.fetchone()
                    conn.commit()

                    if updated_project:
                        print(f"Project with ID {project_id} updated successfully.")
                        print("Updated project:", updated_project)
                        return True
                    else:
                        print(f"No project found with ID {project_id}.")
                        return False
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error updating project {project_id}: {e}")
            conn.rollback()
            return False
    
    @staticmethod
    def delete(project_id:int) -> dict:
        try:
            config = load_config()
            with psycopg.connect(**config) as conn:
                with conn.cursor() as cur:
                    project = Projects.read(project_id)
                    if not project:
                        print(f"Project with ID {project_id} not found.")
                        return {}

                    query = sql.SQL("""
                        DELETE FROM {}.{}
                        WHERE id = %s;
                    """).format(
                        sql.Identifier(Projects.SCHEMA),
                        sql.Identifier(Projects.TABLE)
                    )

                    cur.execute(query, (project_id,))

                    conn.commit()

                    print(f"Project with ID {project_id} deleted successfully.")
                    return project  
        except (Exception, psycopg.DatabaseError) as e:
            print(f"Error deleting project {project_id}: {e}")
            return {}


if __name__ == "__main__":
    pass
