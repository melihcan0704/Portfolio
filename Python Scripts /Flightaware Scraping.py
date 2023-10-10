from datetime import datetime, timedelta
import flightawareparser
from bs4 import BeautifulSoup
import requests
import re
from gtts import gTTS
from playsound import playsound

# Creating CSV at tmp directory
def write_to_file(tail, status, date, csv_name = "last-flights"):
    filename = '/tmp/{}.csv'.format(csv_name)
    data_list = ["{0}, {1}, {2}".format(tail, status, date)]
    with open(filename, 'a') as myfile:
        for data in data_list:
            myfile.write(data + '\n')
    return

facheck= flightawareparser.fascrapper()

number_of_days = 2

flying_hostnames = {}
grounded_hostnames = {}
inactive_hostnames = {}
active_hostnames = {}
error_hostnames = {}
satisfying_hostnames = {}
text = "Last flight script is completed"
tts = gTTS(text)
temp_file = "/home/Desktop/last-flight/temp.mp3"
tts.save(temp_file)

with open("/home/Desktop/last-flight/aircraft_list.txt", 'r') as file:
    for hostname in file:
        hostname = hostname.strip()  # Remove leading/trailing whitespaces and newlines

        if hostname == "Not installed":
            write_to_file(hostname,"G","Skipped")
            print(f"Skipping: {hostname}")
            continue
        try:
            details = facheck.flightdata(hostname)
            date_str = details[8]  # Get the 8th element
            date_obj = datetime.strptime(date_str, '%B %d %Y %H:%M:%S')  # Convert string to datetime object

            if details[4] == "airborne":
                flying_hostnames[hostname] = date_obj
                write_to_file(hostname,"IA",date_obj) #Inserting to last-flights.csv
            elif date_obj < datetime.utcnow() - timedelta(days=7):
                grounded_hostnames[hostname] = date_obj
                write_to_file(hostname,"G",date_obj) #Inserting to last-flights.csv
            elif date_obj < datetime.utcnow() - timedelta(days=1):
                inactive_hostnames[hostname] = date_obj
                write_to_file(hostname,"D",date_obj) #Inserting to last-flights.csv
            elif date_obj >= datetime.utcnow() - timedelta(days=1): #and details[4] != "airborne"
                active_hostnames[hostname] = date_obj
                write_to_file(hostname,"A",date_obj) #Inserting to last-flights.csv

            print(hostname, date_obj)
            if date_obj < datetime.utcnow() - timedelta(days=number_of_days):  # Check if date is older than a number_of_days days
                satisfying_hostnames[hostname] = date_obj  # Add hostname to dictionary
        except Exception as e:
            print(f'Flightaware Failed for {hostname}. Error Code: {str(e)}')
            print('Switching to Radarbox...')
            try:
                url = 'https://www.radarbox.com/data/registration/' + hostname
                r = requests.get(url)
                soup = BeautifulSoup(r.text, "html.parser")
                hour1 = soup.find("div", id="arrival", class_="airport-label")
                hour2 = str(hour1.find("div", id="time"))
                hour3 = re.split('>', hour2)[1].split('<')[0].strip() #last format of time
                lastdate = str(soup.find("div", id="date"))
                lastdate2 = lastdate.split('>')[1].split('<')[0] #last format of date
                lastdate3 = lastdate2.split(',')[1].strip()
                finaldate = lastdate3 + ' ' + hour3 #concatenation of date & time for below line.
                date_obj2 = datetime.strptime(finaldate, '%b %d %Y %H:%M')

                if date_obj2 < datetime.utcnow() - timedelta(days=7):
                    grounded_hostnames[hostname] = date_obj2
                    write_to_file(hostname, "G", date_obj2)
                elif date_obj2 < datetime.utcnow() - timedelta(days=1):
                    inactive_hostnames[hostname] = date_obj2
                    write_to_file(hostname, "D", date_obj2)  # Inserting to last-flights.csv
                elif date_obj2 >= datetime.utcnow() - timedelta(days=1):  # and details[4] != "airborne"
                    active_hostnames[hostname] = date_obj2
                    write_to_file(hostname, "A", date_obj2)  # Inserting to last-flights.csv
                print(hostname, date_obj2)

            except ValueError: #RadarBox occasionally gives error on month type, this will trigger if that happens.
                lastdate4 = datetime.strptime(lastdate3, '%B %d %Y')
                if lastdate4 < datetime.utcnow() - timedelta(days=7):
                    grounded_hostnames[hostname] = finaldate
                    write_to_file(hostname, "G", finaldate)
                elif lastdate4 < datetime.utcnow() - timedelta(days=1):
                    inactive_hostnames[hostname] = finaldate
                    write_to_file(hostname, "D", finaldate)  # Inserting to last-flights.csv
                elif lastdate4 >= datetime.utcnow() - timedelta(days=1):  # and details[4] != "airborne"
                    active_hostnames[hostname] = finaldate
                    write_to_file(hostname, "A", finaldate)  # Inserting to last-flights.csv
                print(hostname, finaldate)

            except Exception as e2: # if all fails AC will be checked manually.
                write_to_file(hostname,"Error",str(e2))
                error_hostnames[hostname] = str(e2) # Add hostname to error list
                print(f"Error occurred for hostname: {hostname}. Error message: {str(e2)}")
                #time.sleep(1)

playsound(temp_file)
import os
os.remove(temp_file)
print()
print(f"The aircrafts that haven't flown for {number_of_days} days:" )
for hostname, date_obj in satisfying_hostnames.items():
    print(hostname, date_obj)

print()
print("Flying aircrafts:")
for hostname, date_obj in flying_hostnames.items():
    print(f"{hostname}: {date_obj}")

print()
print("Grounded aircrafts (Hasn't flown for more than 7 days):")
for hostname, date_obj in grounded_hostnames.items():
    print(f"{hostname}: {date_obj}")

print()
print("Inactive aircrafts (Hasn't flown for 1-7 days):")
for hostname, date_obj in inactive_hostnames.items():
    print(f"{hostname}: {date_obj}")

print()
print("Active aircrafts (Flown in the last 24 hours):")
for hostname, date_obj in active_hostnames.items():
    print(f"{hostname}: {date_obj}")

print()
print("Aircrafts with errors (Check these manually):")
for hostname, error_message in error_hostnames.items():
    print(f"{hostname}: {error_message}")

###REFERENCE
#Sample output for details: ('British Airways 35', 'Boeing 787-9 (twin-jet)', 'London, United Kingdom', 'Chennai / Madras, India', 'airborne', 370, 528, 'November 29 2019 14:30:00', 'November 29 2019 15:01:38', 'November 30 2019 00:03:00', 'November 30 2019 00:13:00', 'November 29 2019 14:33:00', 'November 29 2019 15:01:00', None, None, 'In air, covered 604 nautical miles with 3858 nautical miles remaining.')      

# Order of output:
# Flight number/code
# Aircraft type
# Flight origin
# Flight destination
# Flight status (whether airborne/landed)
# Flight altitude
# Flight ground speed
# Estimated gate departure time
# Estimated takeoff time
# Estimated landing time
# Estimated gate arrival time
# Actual gate departure time
# Actual takeoff time
# Actual landing time
# Actual gate arrival time
# Aircraftposition (If airborne returns distance covered and distance remaining, returns status such as taxiing to takeoff from gate or taxiing to gate after landing)

# Author: Melihcan Sari & Kaan Bereketli
