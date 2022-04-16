import datetime
from datetime import timedelta
import os

from dotenv import load_dotenv
from mysql.connector import Error
import psycopg2


load_dotenv()
database = os.getenv('DATABASE')
password = os.getenv('PASSWORD')


def count_dif() -> None:
    conn = psycopg2.connect(database=database, user='okopkywuaoevjh', password=password,
                                host="ec2-52-3-60-53.compute-1.amazonaws.com", port="5432")
    mydb = conn.cursor()
    mydb.execute(f"SELECT * FROM stock")
    print(mydb.fetchall())

count_dif()