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

date = str(datetime.datetime.today().date())
yesterday = datetime.datetime.today().date() - timedelta(days=1)


def count_dif(day_time: str) -> str:
    """return total and dif"""
    # date = str(datetime.datetime.today().date())
    # yesterday = datetime.datetime.today().date() - timedelta(days=1)
    try:
        conn = psycopg2.connect(database=database, user='okopkywuaoevjh', password=password,
                                host="ec2-52-3-60-53.compute-1.amazonaws.com", port="5432")
        mydb = conn.cursor()
        if day_time == 'morning':
            pass
            mydb.execute(f"SELECT morning FROM cfo_base WHERE date = '{date}'")
            base_now = mydb.fetchone()[0]
            mydb.execute(f"SELECT evening FROM cfo_base WHERE date = '{yesterday}'")
            base_yesterday = mydb.fetchone()[0]
            dif_base = base_now - base_yesterday
            if base_now > base_yesterday:
                text = f'База на утро {date} - {base_now} (+{dif_base})'
            else:
                text = f'База на утро {date} - {base_now} ({dif_base})'
            conn.close()
            return text
        else:
            mydb.execute(f"SELECT evening FROM cfo_base WHERE date = '{date}'")
            base_now = mydb.fetchone()[0]
            mydb.execute(f"SELECT morning FROM cfo_base WHERE date = '{date}'")
            base_morning = mydb.fetchone()[0]
            dif_base = base_now - base_morning
            if base_now > base_morning:
                text = f'Биржа закрывается - {base_now} (+{dif_base})'
            else:
                text = f'Биржа закрывается - {base_now} ({dif_base})'
            conn.close()
            return text
    except Error:
        print('fault with count dif')


def get_previous_value(geo, date, day_time):
    #yesterday = datetime.datetime.today().date() - timedelta(days=1)
    try:
        conn = psycopg2.connect(database=database, user='okopkywuaoevjh', password=password,
                                host="ec2-52-3-60-53.compute-1.amazonaws.com", port="5432")
        mydb = conn.cursor()
        if day_time == 'morning':
            mydb.execute(f"SELECT evening FROM stock WHERE date = '{yesterday}' and region = '{geo}'")
            numb = mydb.fetchone()[0]
        else:
            mydb.execute(f"SELECT morning FROM stock WHERE date = '{date}' and region = '{geo}'")
            numb = mydb.fetchone()[0]
        return numb
    except:
        print("can't get previous count")


def extreme_dif(day_time: str):
    """
    -идем по всем регионам и смотрим разницу
    -фиксируем отклонения более 10% но не менее 30 авто
    :return:
    """
    try:
        conn = psycopg2.connect(database=database, user='okopkywuaoevjh', password=password,
                                host="ec2-52-3-60-53.compute-1.amazonaws.com", port="5432")
        mydb = conn.cursor()
        if day_time == 'evening':
            mydb.execute(f"SELECT (region, morning) FROM stock WHERE date = '{date}'")
            db_morning = mydb.fetchall()
            for i in db_morning:
                pass
            #print(db_morning)
            #for region in  db_morning:

        else:
            pass
    except:
        pass
