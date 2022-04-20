import os
from dotenv import load_dotenv
from mysql.connector import Error
import psycopg2


load_dotenv()
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')


def connect(date, city, day_time, value) -> None:
    """rec data into stock db each one region"""
    try:
        conn = psycopg2.connect(database=database, user='okopkywuaoevjh', password=password,
                                host="ec2-52-3-60-53.compute-1.amazonaws.com", port="5432")
        mydb = conn.cursor()
        if day_time == 'morning':
            mydb.execute(f"INSERT INTO stock (date, region, morning) VALUES ('{date}', '{city}', {value})")

        else:
            mydb.execute(f"UPDATE stock SET evening = {value} WHERE date = '{date}' and region = '{city}'")

        conn.commit()
    except Error:
        print('fault connect')


def record_cfo_base(date: str, day_time: str) -> None:
    """rec data into cfo_base db total count"""
    try:
        conn = psycopg2.connect(database=database, user='okopkywuaoevjh', password=password,
                                host="ec2-52-3-60-53.compute-1.amazonaws.com", port="5432")
        mydb = conn.cursor()
        if day_time == 'morning':
            mydb.execute(f"SELECT SUM (morning) FROM stock WHERE date='{date}'")
            sum_value = int(mydb.fetchone()[0])
            mydb.execute(f"INSERT INTO cfo_base (date, morning) VALUES ('{date}', {sum_value})")
        else:
            mydb.execute(f"SELECT SUM (evening) FROM stock WHERE date='{date}'")
            sum_value = int(mydb.fetchone()[0])
            mydb.execute(f"UPDATE cfo_base SET evening = {sum_value} WHERE date = '{date}'")
        conn.commit()
    except:
        print('fault with recording cfo_base')
