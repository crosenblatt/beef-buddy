import os
import json
import random
import requests
import simplejson

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	query = data['text'].lower()

	if query == 'hi beefbuddy':
		sayHi(data['name'])

	if query == 'beefbuddy, list all commands':


	if 'beefbuddy, flip a coin' in query:
		flipACoin()

	if 'beefbuddy, pick a number' in query:
		nums = [int(s) for s in data['text'].split() if s.isdigit()]
		if len(nums) == 2:
			pickANumber(nums[0], nums[1])

	if 'beefbuddy' in query and 'yes or no' in query:
		if 'is a hot dog a sandwich' in query:
			send_message('yes')
		else:
			yesOrNo()

	if query == 'where is the center of the maze':
		maze()

	if query == 'where is the door':
		door(data['name'])

	return 'OK', 200

def send_message(msg):
	url = 'https://api.groupme.com/v3/bots/post'

	data = {
		'bot_id':os.getenv('GROUPME_BOT_ID'),
		'text':msg,
	}

	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()

def sayHi(name):
	send_message('Hi {}!'.format(name))

def listAllCommands():
	send_message('flip a coin, pick a number, yes or no')

def flipACoin():
	send_message(random.choice['heads', 'tails'])

def pickANumber(start, end):
	send_message(str(random.randint(start, end)))

def yesOrNo():
	send_message(random.choice(['yes', 'no']))

def maze():
	send_message('the maze wasn\'t meant for you')

def door(name):
	send_message('this game was meant for you, {}, but you must play it alone'.format(name))
