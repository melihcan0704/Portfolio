from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
import requests
import json
from gtts import gTTS
from playsound import playsound
import os

scrape_count = 0
text = "Last flight complete"
tts = gTTS(text)
temp_file = "temp.mp3"
tts.save(temp_file)
st= time.time()

def write_to_file(tail, status, date, csv_name = "last-flights"):
    filename = '/tmp/{}.csv'.format(csv_name)
    data_list = ["{0}, {1}, {2}".format(tail, status, date)]
    with open(filename, 'a') as myfile:
        for data in data_list:
            myfile.write(data + '\n')

with open("aircraft_list.txt", 'r') as file:
    for host in file:
        host = host.strip()

        if host =="Not installed":
            write_to_file(host,"G","Skipped")
            print("Skipping: Not installed.")
            continue
        try:
            url = 'https://www.radarbox.com/data/registration/' + host
            time.sleep(1)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            
            #Find values in 'Flight Activity' table
            script_tag = soup.find_all('script', type='module')
            
            #Removing custom website function window.init() so it appears as a JSON body.
            script_tag2 = script_tag[2].text.replace('window.init(','').replace(')','')

            #JSON parsing for the flights table.
            json_parse = json.loads(script_tag2).get('current')
            
            #Get Current AC status
            status=json_parse.get('status')
                     
            if status.strip() == 'estimated':
                utc_year = json_parse.get('lastFlight').get('year_utc')
                utc_day = json_parse.get('lastFlight').get('day_utc')
                utc_time =json_parse.get('lastFlight').get('arre_utc') or json_parse.get('lastFlight').get('arrival_utc') or json_parse.get('lastFlight').get('arrs_utc')
 
            else:

                utc_year = json_parse.get('year_utc')
                utc_day = json_parse.get('day_utc')
                utc_time = json_parse.get('arre_utc') or json_parse.get('arrival_utc') or json_parse.get('arrs_utc')

            #If Arrival time (utc_time) is unknown by the website only scrape date.
            if utc_time is None:
                #Only date (UTC).
                date_string = utc_year +" "+ utc_day
                input_datetime=datetime.strptime(date_string,"%Y %d %b")
                output_datetime=input_datetime.strftime("%d %b %Y")
			#Else date+time
            else:
                #Date & Time (UTC).
                date_string = utc_year +" "+ utc_day +" "+ utc_time
                input_datetime=datetime.strptime(date_string,"%Y %d %b %H:%M")
                output_datetime=input_datetime.strftime("%d %b %Y %I:%M %p")
            
            #Increment scrape count by 1
            scrape_count+=1

            if status == 'live':
                print(host,"| IA |", output_datetime,)
                write_to_file(host,"IA",output_datetime)
                continue #Because it will also write for |A| status.
            
            elif input_datetime < datetime.utcnow() - timedelta(days=7):
                print(host,"| G  |", output_datetime)
                write_to_file(host,"G",output_datetime)
            
            elif input_datetime < datetime.utcnow() - timedelta(days=2):
                print(host,"| D  |", output_datetime)
                write_to_file(host,"D",output_datetime)
            
            elif input_datetime >= datetime.utcnow() - timedelta(days=2):
                print(host,"| A  |", output_datetime)
                write_to_file(host,"A",output_datetime)
            
        except Exception as e:
            print(host, "An Error has occured: ", e)
            write_to_file(host,"E",str(e))

at=time.time()
elapsed_time = at-st
print('\n')            
print("Last Flights Scraped for: ", scrape_count, "Scrape Duration: ", elapsed_time)
playsound(temp_file)
os.remove(temp_file)

#If last flight output for an aircraft is only Date and not Date + Time that is due to website has not updated the 'STA' and 'STATUS' fields in the flights table. Therefore it is blank.

#Author: Melihcan Sariabdullahoglu

