# Bitcoin API

This project is all about building REST api's related to bitcoin using Flask App. Data is taken from [investing.com](https://www.investing.com/crypto/bitcoin/historical-data) and contains bitcoin prices from 1/1/2013 to 30/12/2018. SQL is used to store all the data.

## Installation

venv has all packages needed to run the project succesfully, go to the project folder and run following bash commands.
```bash
virtualenv venv
source venv/bin/activate
python server.py
```
After this step server starts running, try checking on [browser](http://127.0.0.1:5000/).



## API Reference
All api's are GET apis.
### price
Returns bitcoin price info for a [specific day](http://127.0.0.1:5000/price?date=20181201), [last week](http://127.0.0.1:5000/price?last-week=true)(past 7 days) or [last month](http://127.0.0.1:5000/price?last-month=true)(past 30 days). Default is last month.
### map
Returns k days Simple Moving Average Price between start and end date. [This](http://127.0.0.1:5000/map?start=20180112&end=20180113&window=12) is the format of calling api. 
### forecast
Forecasting is done is ARIMA Model which is trained and tuned on all the bitcoin data present in database.
Returns k days of future bitcoin price prediction starting from '20181231', default value of k is 15. [This](http://127.0.0.1:5000/forecast?days=3) is the format of calling api. 
## API Requirements
All dates should be given in yyyymmdd format, e.g. '20180101'.

All api's return json string with a mandatory field "success", if it's value is "false" that means api was unable to process the request due to some reason, if it's "true" then there must be a field "response" which is the actual response of the query.

Dates must be in range of '20130101' to '20181230'.

Bitcoin price data is in bitcoin.csv file.




## Contributing
Suggestions are welcome.