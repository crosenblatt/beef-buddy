import os
import json
import random

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	if data['text'] == 'Hi BeefBuddy':
		msg = 'Hi {}!'.format(data['name'])
		send_message(msg)
	elif data['text'] == 'BeefBuddy, flip a coin':
		flipACoin()



	return 'OK', 200

def send_message(msg):
	url = 'https://api.groupme.com/v3/bots/post'

	data = {
		'bot_id':os.getenv('GROUPME_BOT_ID'),
		'text':msg,
	}

	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()

def flipACoin():
	coin = bool(random.getrandbits(1))
	msg = 'heads' if coin else 'tails'
	send_message(msg)