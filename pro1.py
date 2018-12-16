import os
import time
import glob
from pyrebase import pyrebase
from time import gmtime,strftime
import random

def open_files(lines,name):
    f = open(name,'r')
    for line in f:
        lines.append(line[:-1])
    f.close()
    return lines

def read_temp(sensors_temperature):
    i = 0
    while i<len(sensors_file):
        lines=[]
        open_files(lines,sensors_file[i])
        if (lines[0].strip()[-3:] == 'YES'):
            position = lines[1].find('t=')
            if position != -1:
                temp_string = lines[1][position+2:]
                celsius = float(temp_string) / 1000.0
                sensors_temperature.append(celsius)
        i+=1
    return sensors_temperature

conf = {
    'apiKey': "AIzaSyD39s4Gt4OoLwUActn2l8qDvAe6y9hn2BE",
    'authDomain': "proba-d998d.firebaseapp.com",
    'databaseURL': "https://proba-d998d.firebaseio.com",
    'projectId': "proba-d998d",
    'storageBucket': "proba-d998d.appspot.com",
    'messagingSenderId': "2235652620"
}

firebase=pyrebase.initialize_app(conf)
db = firebase.database()
#db.remove()

path = '/sys/bus/w1/devices/' 
sensors_name_path = glob.glob(path + '28*')
sensors_file = []
i = 0
while i<len(sensors_name_path):
    sensors_file.append((sensors_name_path[i]+ '/w1_slave'))
    i += 1
os.chdir(path)
sensors_name = glob.glob('28*')

current_time=strftime("%H:%M:%S %p",gmtime())
date = strftime("%Y-%b-%d",gmtime())
sensors_temperature = []
read_temp(sensors_temperature)
humidity=str(random.randint(10,100))+"%";
temp_sensor_len = 0
while temp_sensor_len < len(sensors_temperature):
    db.child(date + "-" + current_time).update({"Sensor_" + str(temp_sensor_len +1): sensors_temperature[temp_sensor_len]})
    db.child(date + "-" + current_time).update({"Sensor_" + str(temp_sensor_len + 1) + "_name":sensors_name[temp_sensor_len]})
    temp_sensor_len += 1
db.child(date + "-" + current_time).update({"Time":current_time,"Humidity":humidity,"Date":date})
print(sensors_temperature)
