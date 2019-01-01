from flask import make_response
from datetime import datetime
from datetime import timedelta
import csv

#All configs are done here
DATABASE_NAME = 'historical.db'
JSON_MIME_TYPE = 'application/json'
DATE_LOWER_BOUND = '20130101' 
DATE_UPPER_BOUND = '20181230'
FORECAST_START = '20181231'
DURATION_LIMIT = 365
FILE_NAME = 'bitcoin.csv'
month_name_to_num = {'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 'May' : '05', 'Jun' : '06', 'Jul' : '07', 'Aug': '08', 'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12'}

def import_data_to_sql(db):
	with open(FILE_NAME) as csvfile:
	    reader = csv.reader(csvfile)
	    next(reader, None)
	    for row in reader:
	        month = month_name_to_num[row[0][:3]]
	        day = row[0][4:6]
	        year = row[0][-4:]
	        date = year+month+day
	        price = float(row[1].replace(',',''))
	        open_ = float(row[2].replace(',',''))
	        high = float(row[3].replace(',',''))
	        low = float(row[4].replace(',',''))
	        volume = row[5]
	        change = row[6]
	        query = ('insert into bitcoin ("dt", "price", "open", "high", "low", "volume", "change")'
	        	'VALUES (:dt, :price, :open, :high, :low, :volume, :change);')
	        params = {
	        	"dt" : date, 
	        	"price" : price,
	        	"open" : open_,
	        	"high" : high,
	        	"low" : low,
	        	"volume" : volume,
	        	"change" : change
	        }
	        db.execute(query, params)
	db.commit()

#converts respnse in standard REST api response
def json_response(data = '', status = 200, headers = None):
	headers = headers or {}
	if 'Content-Type' not in headers:
		headers['Content-Type'] = JSON_MIME_TYPE
	return make_response(data, status, headers)


def date_validation(date):
	if date.isdigit() and date >= DATE_LOWER_BOUND and date <= DATE_UPPER_BOUND:
		try:
			datetime.strptime(date, '%Y%m%d')
			return True
		except:
			return False
	return False


def duration_validation(duration): 
	return duration.isdigit() and int(duration) <= DURATION_LIMIT and int(duration) > 0


def validate_map_input(start, end, window):
	if start is None or end is None or window is None:
		return False, "Some fields are missing"
	if date_validation(start) and date_validation(end) and duration_validation(window) and int(end) >= int(start): 
		return True, ""
	return False, "Inconsistent fields"


#function to compute moving averge prices
def get_map(db, start, end, window):
	success, error = validate_map_input(start, end, window)
	if success is False:
		return {"success" : "false", "error" : error}

	window = int(window)
	start = datetime.strptime(start, '%Y%m%d') - timedelta(days=(window-1))
	start = max(start.strftime("%Y%m%d"), DATE_LOWER_BOUND)
	cursor = db.execute('select dt, price from bitcoin where dt >= {0} and dt <= {1};'.format(start, end))
	prices = [(row[0], row[1]) for row in cursor.fetchall()]
	prices.sort()
	current_sum = 0.0
	moving_average = []
	index = 0
	while(index < len(prices)):
		current_sum += prices[index][1]
		if index+1 >= window:
			moving_average.append((prices[index][0], round(current_sum/window, 2)))
			current_sum -= prices[index+1-window][1]
		index += 1
	return {"success" : "true", "response" : moving_average}


#function to compute prices for a specific day, last week or last month
def get_price(db, date, weekly, monthly):
	if date is not None and date_validation(date):
		start = date
		end = date
	elif weekly == "true":
		end = DATE_UPPER_BOUND
		start = datetime.strptime(end, '%Y%m%d') - timedelta(days=7)
		start = start.strftime("%Y%m%d")
	else:
		end = DATE_UPPER_BOUND
		start = datetime.strptime(end, '%Y%m%d') - timedelta(days=30)
		start = start.strftime("%Y%m%d")
	cursor = db.execute('select * from bitcoin where dt >= {0} and dt <= {1};'.format(start, end))
	movement = [{'date' : row[0], 'price' : row[1], 'open' : row[2], 'high' : row[3], 'low' : row[4], 'volume' : row[5], 'percentage_change' : row[6]} for row in cursor.fetchall()]
	return {"success" : "true", "response" : movement}
