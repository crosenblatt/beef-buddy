import os
import json
import random
import datetime
import requests
import pyowm

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	query = data['text'].lower()
	print('{} ID = {}'.format(data['name'], str(data['sender_id'])))

	if 'beefbuddy' in query:
		if query == 'hi beefbuddy':
			sayHi(data['name'])

		if 'flip a coin' in query:
			flipACoin()

		if 'pick a number' in query:
			nums = [int(s) for s in data['text'].split() if s.isdigit()]
			if len(nums) == 2:
				pickANumber(nums[0], nums[1])

		if 'yes or no' in query:
			if 'is a hot dog a sandwich' in query:
				send_message('yes')
			else:
				yesOrNo()

		if 'what can you do' in query:
			listAllCommands()

		if 'tell me the weather' in query:
			getWeather(query.split('in ')[1].title())

		if 'tell me a fact' in query:
			factOfTheDay()

		if 'is today a special day' in query:
			specialDay()

		if 'inspire me' in query or 'inspire us' in query:
			inspire()

		if 'evaluate' in query:
			math(query)

		if 'who made you' in query or 'who created you' in query:
			creatorMessage()

		if 'where is the center of the maze' in query:
			maze()

		if 'where is the door' in query:
			door(data['name'])

	if data['group_id'] == os.getenv('SPAM_GROUP_ID') and 'spam' in query:
		name = ''
		if 'chris' in query:
			name = 'chris'
		elif 'lynn' in query:
			name = 'lynn'
		elif 'bharti' in query:
			name = 'bharti'
		elif 'alex' in query:
			name = 'alex'
		else:
			return

		send_spam(name)

	return 'OK', 200

def send_message(msg):
	url = 'https://api.groupme.com/v3/bots/post'

	data = {
		'bot_id':os.getenv('GROUPME_BOT_ID'),
		'text':msg,
	}

	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()

def send_spam(name):
	name = name.lower()
	msg = ""

	if name == "chris":
		msg = "@Chris Rosenblatt"
	elif name == "lynn":
		msg = "@Alex Lynn Phipps"
	elif name == "alex":
		msg = "@Alex Nguyen"
	elif name == "bharti":
		msg = "@Bharti Mehta"

	url = 'https://api.groupme.com/v3/bots/post'
	data = {
		'bot_id':os.getenv('SPAM_BOT_ID'),
		'text':'@Alex Nguyen',
		'attachments': [
			{
				'type': 'mentions',
				'user_ids': [14774111],
				'loci':[
					[0, 12]
				],
			}
		]
	}

	for i in range(10):
		request = Request(url, urlencode(data).encode())
		json = urlopen(request).read().decode()

def sayHi(name):
	send_message('Hi {}!'.format(name))

def listAllCommands():
	send_message('flip a coin, pick a number, yes or no, tell the weather, tell a random fact, inspire you, recognize special days, evaluate simple math problems')

def flipACoin():
	send_message(random.choice(['heads', 'tails']))

def pickANumber(start, end):
	send_message(str(random.randint(start, end)))

def yesOrNo():
	send_message(random.choice(['yes', 'no']))

def factOfTheDay():
	response = requests.get('http://numbersapi.com/random')
	send_message(response.text)

def getWeather(town):
	try:
		owm = pyowm.OWM(os.getenv('WEATHER_API'))
		obs = owm.weather_at_place('{},US'.format(town))
		w = obs.get_weather()
		temp = w.get_temperature('fahrenheit')['temp']
		send_message(('the current temperature in {} is {} degrees fahrenheit'.format(town, temp).lower()))
	except:
		send_message('sorry, i don\'t know that area')

def specialDay():
	now = datetime.datetime.now()
	bday = ''
	if now.month == 2 and now.day == 22:
		bday = 'chris'
	elif now.month == 11 and now.day == 8:
		bday = 'alex'
	elif now.month == 6 and now.day == 28:
		bday = 'bharti'
	elif now.month == 5 and now.day == 23:
		bday = 'lynn'
	elif now.month == 5 and now.day == 16:
		send_message("happy friendaversary!")
		return

	if bday != "":
		send_message('today is {}\'s birthday! happy birthday!'.format(bday))
	else:
		send_message('not that i know of...')

def inspire():
	response = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json")
	js = json.loads(response.text)
	msg = js['quoteText'] + ' -' + js['quoteAuthor'] if js['quoteAuthor'] != "" else js['quoteText'] + ' -Anonymous'
	send_message(msg)

def math(msg):
	nums = [int(s) for s in msg.split() if s.isdigit()]
	try:
		if len(nums) == 2:
			if '+' in msg:
				send_message(str(nums[0] + nums[1]))
			elif '-' in msg:
				send_message(str(nums[0] - nums[1]))
			elif '*' in msg:
				send_message(str(nums[0] * nums[1]))
			elif '/' in msg:
				send_message(str(nums[0] / nums[1]))
			elif '^' in msg:
				send_message(str(nums[0] ** nums[1]))
			else:
				send_message("sorry, i don't know how to do that. please enter something simpler.")
		else:
			send_message("please enter a valid equation")
	except:
		if nums[0] == 0 and nums[1] == 0 and '/' in msg:
			send_message(
				"""Imagine that you have zero cookies, and you split them evenly among zero friends. How many cookies does each person get? See? It doesn’t make sense. And Cookie Monster is sad that there are no cookies, and you are sad that you have no friends."""
				.lower())
		else:
			send_message("i can't do that")

def creatorMessage():     
	send_message("""I was created by Chris Rosenblatt, a computer science and math student at Purdue University. I also utilize the Numbers API (numbersapi.com), the forismatic API (https://forismatic.com/en/api/) as well as the Open Weather Map API (openweathermap.org) wrapped with the pyowm library (https://github.com/csparpa/pyowm). To find out more about Chris and his projects, visit crosenblatt.me or github.com/crosenblatt.""")

def maze():
	send_message('the maze wasn\'t meant for you')

def door(name):
	send_message('this game was meant for you, {}, but you must play it alone'.format(name))
