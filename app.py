#!/usr/bin/python
import sys
import pprint

import json
import os
import requests
import urllib2, urllib

from flask import Flask
from flask import request
from flask import make_response
from flask import send_file


# Flask app should start in global layout
app = Flask(__name__)
#conn_string = "host='ec2-184-73-167-43.compute-1.amazonaws.com' dbname='d2336hgen7obqh' user='livulrejbcfbvx' password='02c53edb60df98b50cfb1ad8016e5ffe8b24f92eef90bee63ffdc605269e88b2'"
#conn = psycopg2.connect(conn_string)

# conn.cursor will return a cursor object, you can use this cursor to perform queries
#cursor = conn.cursor()

userId = ""

@app.route('/')
def index():
	return "Hello!"


@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)

	print("Request:")
	print(json.dumps(req, indent=4))

	res = makeWebhookResult(req)

	res = json.dumps(res, indent=4)
	print(res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r


def makeWebhookResult(req):
	print(req)

	if req.get("result").get("action") == "get-location":
		city = req.get("result").get("parameters").get("geo-city")
		baseurl = "https://query.yahooapis.com/v1/public/yql?"
		#yql_query = "select wind from weather.forecast where woeid=2460286"
		yql_query = 'select item.condition.text from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+city+'")'
		yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
		result = urllib2.urlopen(yql_url).read()
		data = json.loads(result)

		if results is not None:
			condition = data['item']['condition']['text']
			print(condition)
			#{u'channel': {u'item': {u'condition': {u'text': u'Partly Cloudy'}}}}
		#print(data['query']['results'])




if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print("Starting app on port %d" % port)

	app.run(debug=True, port=port, host='0.0.0.0')
	# print the connection string we will use to connect
	#print("Connecting to database\n ->%s" % (conn_string))
