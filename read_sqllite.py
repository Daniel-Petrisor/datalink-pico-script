
from cmath import e
from datetime import datetime, timedelta
import sqlite3
from statistics import median, mean

# get the current datetime and store it in a variable
currentDateTime = datetime.now()
string_dt = currentDateTime.strftime("%d/%m/%Y %H:%M")


hours = 0
minutes = 10

current_data = datetime.now() - timedelta(hours=0, minutes=2)
current_string_dt = current_data.strftime("%d/%m/%Y %H:%M")

work_time = timedelta(hours=hours, minutes=minutes)
work_start = "2022-09-28 17:53" #current_data
work_end = "2022-09-28 18:00" # work_start + work_time




def read_last_data(path_dir, sensor_name, n_row):
    connection  = sqlite3.connect(path_dir, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor  = connection.cursor()

    # select query to retrieve last row
    cursor.execute(f"SELECT * from '{sensor_name}' ORDER BY datetime DESC LIMIT '{n_row}'")
    last_row = cursor.fetchall()

    # to access specific fetched data
    for row in last_row:
        data = row[0]
        forno = row[1]
        temperatura = row[2]
        print("Last :", data, forno, temperatura)
    # commit the changes,
    # close the cursor and database connection
    cursor.close()
    connection.close()




def read_interval_data(path_dir, sensor_name, dt_start, dt_end):

    t_val = []

    connection  = sqlite3.connect(path_dir, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor  = connection.cursor()

    # select query to retrieve data
    cursor.execute(f"SELECT * from '{sensor_name}' where datetime >= '{dt_start}' and datetime <='{dt_end}'")
    fetchedData = cursor.fetchall()

    # to access specific fetched data
    for row in fetchedData:
        date = row[0]
        sensore = row[1]
        temperatura = row[2]
        t_val.append(temperatura)
        print(date, sensore, temperatura)

    # commit the changes,
    # close the cursor and database connection
    cursor.close()
    connection.close()

    # Statistic value
    maximum = max(t_val)
    minimum = min(t_val)
    avg_value = mean(t_val)
    median_value = median(t_val)

    # Time for records (1 row = 1 minute)
    # ! Check integrity records (compare with interval date )
    row_records = len(t_val)
    hour = row_records // 60
    minute = row_records % 60

    # Print statistic values 
    print(f'''
    Start: {dt_start} - End: {dt_end}
    Total time: {hour}:{minute} | Records: {row_records}
    Max value: {maximum}
    Min value: {minimum}
    Median value: {median_value}

    AVG: {avg_value}

    ''')






path_sqlite3 = "W:\Altri computer\Produzione 1\Pico Technology\EnviroMon\Data\produzione1.sqlite3"
date_start = "06/10/2022 11:10:00"
date_end = "07/10/2022 02:40:00"
forno = "OSAR 7"

try:
    read_interval_data(path_sqlite3, forno, date_start, date_end)
except:
    print("Dati non disponibili per l'intervallo selezionato")


read_last_data(path_sqlite3, forno, 1)