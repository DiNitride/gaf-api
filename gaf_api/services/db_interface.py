import psycopg2
import logging

from ..tools import utils

db_config = utils.load_config("db.json")

conn_string = f"" \
              f"host='{db_config['host']}' " \
              f"dbname='{db_config['db']}' " \
              f"user='{db_config['db_user']}' " \
              f"password='{db_config['db_pass']}'"

conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

logger = logging.getLogger(__name__)

# TODO: Add logging to all of these functions
# TODO: Also add try/catch?


def get_user(user_id: int):
    cursor.execute("SELECT * FROM users WHERE id=(%s)", (user_id,))
    user = cursor.fetchone()
    logger.debug(f"Fetched user {user}")
    return user


def add_user(user_id: id, access_token: str, refresh_token: str):
    user = get_user(user_id)
    if user is not None:
        return
    cursor.execute("INSERT INTO users VALUES (%s, %s, %s)", (user_id, access_token, refresh_token))
    conn.commit()


def remove_user(user_id: int):
    cursor.execute("DELETE FROM users WHERE id=(%s)", (user_id,))
    conn.commit()


def get_acronym_by_id(id: int):
    cursor.execute("SELECT * FROM acronyms WHERE id=(%s)", (id,))
    return cursor.fetchone()


def get_acronym_by_name(acronym: str):
    cursor.execute("SELECT * FROM acronyms WHERE acronym=(%s)", (acronym,))
    return cursor.fetchone()


def get_all_acronyms():
    cursor.execute("SELECT * FROM acronyms")
    return cursor.fetchall()


def check_for_acronym(acronym: str):
    cursor.execute("SELECT * FROM acronyms WHERE LOWER(acronym) LIKE (%s)", (acronym,))
    return cursor.fetchone()


def add_acronym(acronym: str):
    if check_for_acronym(acronym.lower()) is None:
        cursor.execute("INSERT INTO acronyms VALUES (DEFAULT, %s)", (acronym,))
        conn.commit()
        return True
    return False


def del_acronym(id: int):
    cursor.execute("DELETE FROM acronyms WHERE id=(%s)", (id,))
    conn.commit()
