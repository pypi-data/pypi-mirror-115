import requests
import pandas as pd
import json
from datetime import datetime
from google.cloud.sql.connector import connector
from threading import Timer
import mysql.connector

def data_extraction():
    end_date = datetime.today().strftime('%Y-%m-%d')
    print("test")
    print(end_date)
    print("test")

    #URL FOR BALI TO CENTRAL JAVA:
    #url = "https://destinationinsights.withgoogle.com/data/daily?origin_country=ID&destination_country=ID&travel_type=FLIGHT&trip_type=DOMESTIC&date_start=2021-04-07&date_end=" + end_date + "&destination_admin_area=Central%20Java&origin_admin_area=Bali"

    #URL FOR JAKARTA TO EAST JAVA:
    url = "https://destinationinsights.withgoogle.com/data/daily?origin_country=ID&destination_country=ID&travel_type=FLIGHT&trip_type=DOMESTIC&date_start=2021-04-07&date_end=" + end_date + "&destination_admin_area=East%20Java&origin_admin_area=Jakarta"
    r = requests.get(url)
    data = json.loads(r.text)
    var = json.dumps(data['daily_travel_demand'])
    df_json = pd.read_json(var)

    #creating CSV file:
    df_json.to_csv('test_pandas.csv')

    #file uploading to SQL server:
    read_file = pd.read_csv(r'/Users/juliantanja/PycharmProjects/INTERNSHIP2.1/test_pandas.csv')

    df = pd.DataFrame(read_file, columns= ['date', 'current_market_queries', 'last_year_market_queries'])
    print(df)

    #Creating an SQL database:
    my_db = mysql.connector.connect(host="localhost", user="root", password="Singap0r3", database="tiketinternship")
    cursor = my_db.cursor()

    #Deleting old data/emptying database:
    print("deleting all rows in table")
    delete_sql = "DELETE FROM data_insights2"
    cursor.execute(delete_sql)
    print("deleting data success")


    #Inserting CSV file into SQL database TABLE:
    for i, row in df.iterrows():
        print(i, row[0], row[1], row[2])
        sql = "INSERT INTO data_insights2 (Nomor, Tanggal, current_queries, lastyear_queries) VALUES (%s, %s, %s, %s)"
        val = (i, row[0], row[1], row[2])
        cursor.execute(sql, val)
        print("Record inserted.")

    my_db.commit()
    print("Success")

#schedule.every().day.at("01:00").do(data_extraction)

#while True:
    #schedule.run_pending()
    #time.sleep(1)


#origin jawa timur/jakarta/jawabarat --> destination all destinations. ALL IN ONE GRAPH
#baseline all indonesia to all indonesia.
