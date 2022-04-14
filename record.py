import datetime

from mysql.connector import Error
import psycopg2


def connect(date, city, day_time, value):
    try:
        conn = psycopg2.connect(database="d4mk95ai4ne4b2", user="okopkywuaoevjh",
                            password="3d6cd73a289ad4df33ab24c227129ef9d8678816162bd12527d8b0f681054fd2",
                            host="ec2-52-3-60-53.compute-1.amazonaws.com", port="5432")
        mydb = conn.cursor()
        if conn:
            print('Connection - record')
        if day_time == 'morning':
            mydb.execute(f"INSERT INTO base (date, reg, morning) VALUES ('{date}', '{city}', {value})")
        else:
            #mydb.execute(f"INSERT INTO base (evening) VALUES ({value}) WHERE morning = 1100")
            mydb.execute(f"INSERT INTO base (date, reg, evening) VALUES ('{date}', '{city}', {value})")
            #print(mydb.fetchall())
        conn.commit()
        conn.close()

    except Error:
            print('SQL is not available now')

date = str(datetime.datetime.today().date())
#print(date)
# city = 'lip'
# connect(date, city, 'evening', 1200)
