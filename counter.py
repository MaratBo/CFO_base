import datetime
from datetime import timedelta
import os

from dotenv import load_dotenv
from mysql.connector import Error
import psycopg2

load_dotenv()
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')


def count_dif(day_time) -> str:
    """return total and dif"""
    date = str(datetime.datetime.today().date())
    yesterday = datetime.datetime.today().date() - timedelta(days=1)
    try:
        conn = psycopg2.connect(database=database, user='okopkywuaoevjh', password=password,
                                host="ec2-52-3-60-53.compute-1.amazonaws.com", port="5432")
        mydb = conn.cursor()
        if day_time == 'morning':
            pass
            base_now = mydb.execute(f"SELECT morning FROM cfo_base WHERE date = '{date}'")
            base_yesterday = mydb.execute(f"SELECT evening FROM cfo_base WHERE date = '{yesterday}'")
            dif_base = base_now - base_yesterday
            if base_now > base_yesterday:
                text = f'База на {date} - {base_now} (+{dif_base})'
            else:
                text = f'База на {date} - {base_now} ({dif_base})'
            conn.close()
            return text
        else:
            mydb.execute(f"SELECT evening FROM cfo_base WHERE date = '{date}'")
            base_now = mydb.fetchone()[0]
            mydb.execute(f"SELECT morning FROM cfo_base WHERE date = '{date}'")
            base_morning = mydb.fetchone()[0]
            dif_base = base_now - base_morning
            if base_now > base_morning:
                text = f'Текущая база - {base_now} (+{dif_base})'
            else:
                text = f'Текущая база - {base_now} ({dif_base})'
            conn.close()
            return text
    except Error:
        print('fault with count dif')
