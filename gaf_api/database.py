import psycopg2
import pprint

from gaf_api.services import utils


db_config = utils.load_config("db.json")

conn_string = f"" \
              f"host='localhost' " \
              f"dbname='dev-NeverEndingGAF' " \
              f"user='{db_config['db_user']}' " \
              f"password='{db_config['db_pass']}'"

conn = psycopg2.connect(conn_string)
cursor = conn.cursor()


def get_user(user_id: int):
    cursor.execute("SELECT * FROM public.users WHERE id=(%s)", (user_id,))
    user = cursor.fetchone()
    pprint.pprint(user)
    return user


def add_user(user_id: id, access_token: str, refresh_token: str):
    user = get_user(user_id)
    if user is not None:
        print("User already exists, not creating a new one")
        return
    cursor.execute("INSERT INTO public.users VALUES (%s, %s, %s)", (user_id, access_token, refresh_token))
    conn.commit()
    print("Created new user in DB")


def remove_user(user_id: int):
    cursor.execute("DELETE FROM public.users WHERE id=(%s)", (user_id,))
    conn.commit()
    print("removed user")
