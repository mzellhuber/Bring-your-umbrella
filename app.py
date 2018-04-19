#!/usr/bin/python
# -*- coding: utf-8 -*-
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

	if req.get("queryResult").get("action") == "get-location":
		city = req.get("queryResult").get("parameters").get("geo-city")
		city = city.encode('utf8')
		baseurl = "https://query.yahooapis.com/v1/public/yql?"
		#yql_query = "select wind from weather.forecast where woeid=2460286"
		yql_query = 'select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+city+'")'
		yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
		result = urllib2.urlopen(yql_url).read()
		data = json.loads(result)
		#print(data)
		#print(data['query']['results'])

		if data is not None:
			condition_text = data['query']['results']['channel']['item']['condition']['text']
			condition_code = data['query']['results']['channel']['item']['condition']['code']
			#print(condition_text)
			#print(condition_code)

			if int(condition_code) in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,35,37,38,39,40,41,42,43,45,46,47]:
				#print("bring umbrella")
				umbrella = "🌧"
				umbrella = umbrella.decode('utf-8')

				text = "It looks like the weather for "+city+" is "+condition_text+". You should bring an umbrella."+umbrella

				return {
						"fulfillmentText": text,
						"payload": {
						  "facebook": {
						    "text": text
						  },
						  "slack": {
						    "text": text
						  }
						}
						}
			else:
				#print("not umbrella")
				text = "It looks like the weather for "+city+" is "+condition_text+". You don't need an umbrella."

				return {
						"fulfillmentText": text,
						"payload": {
						  "facebook": {
						    "text": text
						  },
						  "slack": {
						    "text": text
						  }
						}
						}




if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print("Starting app on port %d" % port)

	app.run(debug=True, port=port, host='0.0.0.0')
	# print the connection string we will use to connect
	#print("Connecting to database\n ->%s" % (conn_string))
