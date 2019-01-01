from statsmodels.tsa.arima_model import ARIMA
from datetime import datetime
from datetime import timedelta

from pandas import read_csv
from utils import month_name_to_num, FORECAST_START, duration_validation, FILE_NAME

class forecast_helper():

	def __init__(self):
		self.model = None
		self.filename = FILE_NAME

	#builds the model by reading all data from csv 
	def build(self):
		series = read_csv(self.filename, header=0, parse_dates=[0], index_col=0, squeeze=True, usecols=['Date','Price'])
		series = series.apply(lambda x : float(x.replace(',','')))
		X = series.values[::-1]
		model = ARIMA(X, order=(5,1,3))
		model_fit = model.fit(disp=0)
		self.model = model_fit

	#makes prediction for next 'days' days of prices
	def predict(self, days='15'):
		if duration_validation(days) and int(days) <= 30:
			days = int(days)
			prices = self.model.forecast(days)[0]
			current_day = datetime.strptime(FORECAST_START, '%Y%m%d')
			forecasted_values = []
			for index in range(0, len(prices)):
				date = current_day.strftime("%Y%m%d")
				forecasted_values.append((date, round(prices[index], 2)))
				current_day += timedelta(days=1)
			return {"success" : "true", "response" : forecasted_values}
		else:
			return {"success" : "false", "response" : "incorrect input"}





