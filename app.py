from __future__ import print_function # In python 2.7

from twilio import twiml

from twilio.rest import Client

from flask import Flask, jsonify
from flask import request, redirect

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse


import sys
import logging
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


app = Flask(__name__)

cred = credentials.Certificate('service.json')
firebase_admin.initialize_app(cred, {
   "databaseURL": "https://globalhacks7.firebaseio.com",
})


	
# 127.0.0.1:5000/register?phone=1234&name=Jay&location=saintLouis&nationality=Indian&messengerType=Whatsapp&groupName=Trial
@app.route('/registerPatron', methods=['GET'])
def register_patron():
	args = request.args
	phone = args['phone']
	location = args['location']
	nationality = args['nationality']
	messengerType = args['messengerType']
	groupName = args['groupName']
	name = args['name']

	data = {"name":name, "phone": phone, "location": location, "nationality": nationality, "messengerType": messengerType, "groupName": groupName}
	
	root = db.reference()
	ref  = root.child('patron')	
	userRef = ref.push(data)
	return "Success"


@app.route('/registerImmigrant', methods=['GET'])
def register_immigrant():
	args = request.args
	phone = args['phone']
	name = args['name']
	patronPhone = args['patronPhone']

	val = list(db.reference('patron').order_by_child("phone").equal_to(patronPhone).get().values())[0]
	location = val['location']
	nationality = val['nationality']
	groupName = val['groupName']
	messengerType = val['messengerType']
	
	data = {"name":name, "phone": phone, "location": location, "patronPhone": patronPhone, "nationality": nationality, "messengerType": messengerType, "groupName": groupName}
	
	root = db.reference()
	ref  = root.child('immigrants')	
	userRef = ref.push(data)
	return "Success"


#127.0.0.1:5000/postEvent?event=LOLOLOL&patronPhone=12345&messengerType=FB
@app.route('/postEvent', methods=['GET'])
def post_events():
	args = request.args
	eventData = args['event']
	messengerType = args['messengerType']
	patronNumber = str(args['patronPhone'])

	val = list(db.reference('patron').order_by_child("phone").equal_to(patronNumber).get().values())[0]
	location = val['location']
	nationality = val['nationality']
	groupName = val['groupName']
	data = {"event":eventData, "patronPhone": patronNumber, "location": location, "nationality": nationality, "messengerType": messengerType, "groupName": groupName}
	root = db.reference()
	new_user = root.child('events').push(data)

	return "Success"

#http://127.0.0.1:5000/getEvent?location=NYC
@app.route('/getEvent', methods=['GET'])
def get_events():
	args = request.args
	if "location" in args:
		val = list(db.reference('events').order_by_child("location").equal_to(args['location']).get().values())
	else:
		val = list(db.reference('events').get().values())
	
	return str(val)

			
@app.route('/postQuery', methods=['GET'])
def post_query():
	args = request.args
	phoneNumber = args['phone']
	nationality = args['nationality']
	messenger = args['messenger']
	query = args['query']
	
	data = {"phone":phoneNumber, "nationality": nationality, "messenger": messenger, "query": query}
	root = db.reference()
	new_user = root.child('queries').push(data)

	return "Success"

@app.route('/getQuery', methods=['GET'])
def get_queries():
	args = request.args
	if "location" in args:
		val = list(db.reference('queries').order_by_child("location").equal_to(args['location']).get().values())
	else:
		val = list(db.reference('queries').get().values())
	
	return str(val)

@app.route('/sendWhatsAppMessage', methods=['GET'])
def send_WP_message():
	args = request.args
	to = args['to']
	message = args['message']
	
	
	from twilio.rest import Client

	account_sid = 'ACe58e52bde56b9659bb7dfe80653d31b6'
	auth_token = '4572801f338e4e4f94d4772985e130ec'
	client = Client(account_sid, auth_token)

	message = client.messages.create(
					body=message,
					from_='whatsapp:+14155238886',
					to='whatsapp:+16319979047'
				)

	print(message.sid)

	return "Success"

@app.route('/getWhatsAppMessage', methods=['POST'])
def handle_get_WP_message():
	body = request.values.get('Body', None)

	from TwitterAPI import TwitterAPI
  
	# personal details 
	consumer_key ="5YGcUrIGaEk9HMo9niSiv3elv"
	consumer_secret ="3QPKtpIUtWb2m1NWmjhKi4szhCporKOEC84sEJer9Oo8VHazx3"
	access_token ="2405586890-Gj5ThOKtDIedJneZhXeNpV2WL8S5zLxgBk17O69"
	access_token_secret ="f2wBmpZ23mFahiK3P7sjgONPFqSymawL7ZU8Yxh8fyFEG"
	
	api = TwitterAPI(consumer_key,
                 consumer_secret,
                 access_token,
                 access_token_secret)

	r = api.request('statuses/update', {'status': body})
	print ('SUCCESS' if r.status_code == 200 else 'FAILURE')

	resp = MessagingResponse()
	resp.message(body)

	return str(resp)

if __name__ == '__main__':
    app.run(debug=True)