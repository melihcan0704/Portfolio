### This python class scrapes the latest flight information of a given tail id or flight number from Radarbox.com

## Examples & Output:

```python
import ac_parser

acinfo=ac_parser.aircraft_scrape()

```

When class is defined available functions are:

acinfo.report_status('Your input')

acinfo.current_status('Your input')

acinfo.isgrounded('Your input')

Input should either be an aircraft tail or a flight number. Otherwise it give raise an exception.

