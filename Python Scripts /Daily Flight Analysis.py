#!/usr/bin/env python
# coding: utf-8
from datetime import time,datetime
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import json
import time as t


def write_to_file(tail, duration, csv_name = "average-flight-duration"):
    filename = '/tmp/{}.csv'.format(csv_name)
    data_list = ["{0}, {1}".format(tail, duration)]
    with open(filename, 'a') as myfile:
        for data in data_list:
            myfile.write(data + '\n')

with open("aircraft_list.txt", 'r') as file:
    for host in file:
        host = host.strip()

        try:
            url = 'https://www.radarbox.com/data/registration/' + host
            t.sleep(1)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            script_tag = soup.find_all('script', type='module')
            script_tag2 = script_tag[2].text.replace('window.init(','').replace(')','')
            json_parse = json.loads(script_tag2)
            flight_data=json_parse.get('list')

            # Function to parse a duration string "01h45m" and convert it to a time object
            def parse_duration(duration_str):
                hours, minutes = map(int, duration_str[:-1].split('h'))
                return time(hours, minutes)

            date_durations = defaultdict(list)

            for v in flight_data.values():
                if not isinstance(v, bool):
                    for a in v:
                        date = a['day_utc']
                        duration_str = a['duration']
                        try:
                            duration = parse_duration(duration_str)
                            date_durations[date].append(duration)
                        except Exception:
                            continue
            # Calculate average duration for each date
            average_durations = {}
            total_seconds = 0
            total_durations = 0

            for date, durations in date_durations.items():
                total_seconds_date = sum(map(lambda x: x.hour * 3600 + x.minute * 60, durations))
                average_seconds = total_seconds_date / len(durations)
                average_hours = int(average_seconds // 3600)
                average_minutes = int((average_seconds % 3600) // 60)
                average_duration = time(average_hours, average_minutes)
                average_durations[date] = average_duration

                total_seconds += total_seconds_date
                total_durations += len(durations)

            # Calculate the total average duration
            total_average_seconds = total_seconds / total_durations
            total_average_hours = int(total_average_seconds // 3600)
            total_average_minutes = int((total_average_seconds % 3600) // 60)
            total_average_duration = time(total_average_hours, total_average_minutes)

            # Now 'average_durations' is a dictionary with dates as keys and average durations as time objects

            # Print the result
            print("----------- ",host," ----------")
            print('   Date    |  DF | Avg. Duration') #DF: Daily number of flights.
            print(' ----------------------------- ')
            for date, average_duration in average_durations.items():
                date_obj = datetime.strptime(date, '%d %b')  # Convert date string to datetime object
                formatted_date = date_obj.strftime('%d %b')
                print("| ",formatted_date," | ",len(date_durations[date])," |   ",average_duration.strftime('%Hh%Mm'),"  |")
            print('-------------------------------')
            print(" Total Average:      ", total_average_duration.strftime('%Hh%Mm'))
            print("\n")

            write_to_file(host,total_average_duration.strftime('%Hh%Mm'))

        except Exception as e:
            print(host,"Error: ", str(e))
            write_to_file(host,"")


#Example Output:
# -----------  EC-NTU  ----------
#    Date    |  DF | Avg. Duration
#  -----------------------------
# |  28 Nov  |  3  |    01h30m   |
# |  26 Nov  |  4  |    01h04m   |
# |  24 Nov  |  4  |    01h08m   |
# |  23 Nov  |  4  |    01h17m   |
# -------------------------------
#  Total Average:       01h14m
