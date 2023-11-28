## Jira Ticket Automation

This script automates the ticket opening phase from the service desk. It takes a csv file as a reference and fields inside.
The parameteres inside the csv will be filled with accordingly to the json body of the project.

## Flight Aware Scraping
This script scrapes flight data of a given tail id and pastes the time information of the last completed flight on a csv file.
The script initially uses the FA Parser class (https://github.com/shivasiddharth/Flightaware-Parser.git). We have adjusted the scraped data as per our needs and optimized certain aspects to improve its performance.
The script occasionally fails to pull data from Flightaware due to time out error, so I added an another website to scrape in case of a failure.

## Radarbox Scraping

Radarbox.com is an open source aviation website that allows all sorts of scraping from their website without blocking any of the requests sent.
The script is similar to the Flightaware Scraping script but adjusted for this websites html structure.
Each loop takes the tail id's from aircraft.txt file and returns the status, arrival date & time of the last completed flight in a csv file.

## Daily Flights Analysis

Given a tail id from the aircraft.txt file the script returns the number of completed flights, average duration of all flights for each day.
For each tail it will only return the analysis for last 7 days.
It will also return the overall average for the last 7 days.
An example output has been provided inside the script.
