import psycopg2
from psycopg2 import sql
from os import getenv

# use stable client
client = psycopg2.connect(
    host=getenv("POSTGRES_HOST"),
    port=getenv("POSTGRES_PORT"),
    database=getenv("POSTGRES_DB"),
    user=getenv("POSTGRES_USER"),
    password=getenv("POSTGRES_PASSWORD"),
)


def execute_query(query):
    with client.cursor() as cursor:
        cursor.execute(sql.SQL(f"{query};"))
        if cursor.description:  # if the query returns rows
            return cursor.fetchall()
        else:
            client.commit()  # commit changes for non-select queries
            return None
