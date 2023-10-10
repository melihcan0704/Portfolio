## Jira Ticket Automation

This script automates the ticket opening phase from the service desk. It takes a csv file as a reference and fields inside.
The parameteres inside the csv will be filled with accordingly to the json body of the project.

## Flight Aware Scraping
This script scrapes flight data of a given tail id and pastes the time information of the last completed flight on a csv file.
The script initially uses the FA Parser class (https://github.com/shivasiddharth/Flightaware-Parser.git). We have adjusted the scraped data as per our needs and optimized certain aspects to improve its performance.
The script occasionally fails to pull data from Flightaware due to time out error, so I added an another website to scrape in case of a failure.
