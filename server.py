from flask import Flask, request, jsonify, g
import sqlite3
import json
from utils import json_response, get_map, JSON_MIME_TYPE, import_data_to_sql, get_price, DATABASE_NAME
from forecast import forecast_helper
from flask.cli import with_appcontext
import click


app = Flask(__name__)
app.config.from_object(__name__)

#Imports CSV data to SQL Database and initializes the forecasting model
@app.before_request
def before_request():
	g.db = init_db()
	import_data_to_sql(g.db)
	if 'forecaster' not in g:
		forecaster = forecast_helper()
		forecaster.build()
		g.forecaster = forecaster


def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			app.config['DATABASE_NAME'],
			detect_types=sqlite3.PARSE_DECLTYPES
	    )
	g.db.row_factory = sqlite3.Row
	return g.db


def close_db(e=None):
	db = g.pop('db', None)
	if db is not None:
		db.close()


def init_db():
	db = get_db()
	with app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))
	return db

#homepage
@app.route("/")
def hello():
	return "Happy new year from Vivek, this project provides apis related to bitoin price movement and forecasting."


#returns simple moving average price
@app.route('/map')
def map():
	try:
		start = request.args.get('start')
		end = request.args.get('end')
		window = request.args.get('window')
		response = get_map(g.db, start, end, window)
		return json_response(json.dumps(response))
	except:
		response = json.dumps({'error' : 'Unknown', 'success' : 'false'})
		return json_response(response, 404)


#returns pricing infor for a specific date, last week or last month
@app.route('/price')
def price():
	try:
		date = request.args.get('date')
		weekly = request.args.get('last-week')
		monthly = request.args.get('last-month')
		response = get_price(g.db, date, weekly, monthly)
		return json_response(json.dumps(response))   
	except:
		response = json.dumps({'error' : 'Unknown', 'success' : 'false'})
		return json_response(response, 404)


#returns forecasted prices for next k days starting from '20183012'
@app.route('/forecast')
def forecast():
	try:
		days = request.args.get('days')
		response = g.forecaster.predict(days) if days is not None else g.forecaster.predict()
		return json_response(json.dumps(response))
	except:
		response = json.dumps({'error' : 'Unknown', 'success' : 'false'})
		return json_response(response, 404)



if __name__ == '__main__':
	app.run(debug=True)