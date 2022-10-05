import os
import json
import sqlite3
import time

from datetime import datetime
from configparser import ConfigParser


class Datalink:

    def read_last_update_file(current_file_path):
        ''' Return last update date time '''
        # Read metadata source file
        input_file = os.stat(current_file_path)
        dt_file = datetime.fromtimestamp(input_file.st_mtime)
        return dt_file


    def read_current_file(current_file_path):
        '''
        Read current file from logger directory
        Return Dictionary:
        - Key: sensor name
        - Value: sensor value
        '''
        data = []
        labels = []
        sensorDict = dict()

        with open(current_file_path, 'r') as text_file:
            # Read last update file ( date and time )
            dt_file = Datalink.read_last_update_file(current_file_path)
            string_dt_file = dt_file.strftime("%d/%m/%Y %H:%M")

            # Read content source file
            for line in text_file :
                tempDict = dict()
                if "," in line :
                    parts = line.split(",")
                    sensor_name = parts[1].replace('"', "")
                    sensor_value = float(parts[2]+"."+parts[3])

                    labels.append(sensor_name)
                    data.append(sensor_value)
                    tempDict = dict(zip(labels, data))
                    # sensorDict[sensor_name] = sensor_value

        sensorDict = {
            'datetime': string_dt_file,
            'sensors': tempDict
        }
        return sensorDict


    def stored_data(current_data, output_sqlite3, output_json, save_json):
        # Local date time
        now = datetime.now()
        dt_now = now.strftime("%d/%m/%Y %H:%M:%S")


        # Export in sqlite3
        con = sqlite3.connect(output_sqlite3)
        cur = con.cursor()
        for sensor_name, sensor_value in current_data['sensors'].items():
            dt = current_data['datetime']
            print(dt, sensor_name, sensor_value)

            # Create table
            cur.execute("CREATE TABLE IF NOT EXISTS '"+str(sensor_name)+"' (datetime text, sensor text, temperature real, unit text, created text)")
            # Insert a row of data
            cur.execute("INSERT INTO '"+str(sensor_name)+"' VALUES ('"+str(dt)+"','"+str(sensor_name)+"', '"+str(sensor_value)+"', '"+str("°C")+"', '"+str(dt_now)+"')")
            # Save (commit) the changes
            con.commit()
            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            # close the cursor and database connection
        cur.close()
        con.close()


        # Export in json
        if save_json == "Yes":
            tempDict = {
                'created':dt_now,
                'dataset':current_data
            }
            lst=[]
            lst.append(tempDict)
            with open(output_json, 'a') as json_file:
                json.dump(lst, json_file)
                json_file.write(',\n')







def run_App(config_path):
    # Read config file and set output directory
    if os.path.exists(config_path):
        # Reading the file
        config = ConfigParser()
        source = config.read(config_path)
        sections_lst = config.sections()

        # Extracting values.
        # logger_name = config.get('Datalink','LoggerName')
        # update_date = config.get('Datalink','SecondsPerReading')
        current_file_path = config.get('Datalink','CurrentFile')
        output_sqlite_path = config.get('Datalink','DataBasePath')
        output_json_path = config.get('Datalink','JsonFilePath')
        save_json_value = config.get('Datalink','SaveJsonData')

        print(f'''
        CurrentFile : {current_file_path}
        DataBasePath : {output_sqlite_path}
        JsonFilePath : {output_json_path}
        SaveJsonData : {save_json_value}
        ''')



    # Read last update datetime from the current file
    last_dt = Datalink.read_last_update_file(current_file_path)
    print("Last update :", last_dt)
    print("Waiting for new data ... ")
    print("")

    while True:
        now = datetime.now()
        dt_now = now.strftime("%d/%m/%Y %H:%M:%S")
        # localtime = time.localtime()
        # result = time.strftime("%I:%M:%S %p", localtime)
        time.sleep(1)

        new_dt = Datalink.read_last_update_file(current_file_path) # Read last update file ( datetime )
        # Check new update file
        if new_dt > last_dt:
            last_dt = new_dt
            delta = now - new_dt
            seconds = delta.seconds
            print("Date :", dt_now, " | ", "Delay :", seconds,"s")
            
            current_file = Datalink.read_current_file(current_file_path) # Read current file from logger directory
            Datalink.stored_data(current_file, output_sqlite_path, output_json_path, save_json_value) # Stored data in sqlite3 and json

            print("Waiting for new data ... ")
            print("")



config_dir_path = os.path.dirname(os.path.realpath(__file__)) + '\config.ini'
run_App(config_dir_path)







