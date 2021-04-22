#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import requests 
import json 
import os

CONSUMER_KEY= os.environ['CONSUMER_KEY']
CONSUMER_SECRET =os.environ['CONSUMER_SECRET']
ACCESS_TOKEN= os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET =os.environ['ACCESS_TOKEN_SECRET']
BITLY_TOKEN = os.environ['BITLY_TOKEN']



resp = requests.get("https://www.saludcastillayleon.es/en/covid-19-poblacion/vacunacion-covid/lugares-vacunacion/leon")
citas = resp.text.count("/en/covid-19-poblacion/vacunacion-covid/lugares-vacunacion/leon.files/")
resp = resp.text.split('<li class="cmResourceType_pdf cmResourceItem cmOneResourceFile firstNode">')[1].split("</div>")[0]
lugares = {}
archivo = {}

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


for i in range (citas):
	i = i+1
	lugares[i] = resp.split('<span class="resourceData2">')[i].split('</span>')[0]
	lugares[i] = lugares[i].replace("_", " ")
	lugares[i] = lugares[i].replace("compressed", "")
	lugares[i] = lugares[i].replace("-0", "")

	archivo[i] = "https://www.saludcastillayleon.es"
	archivo[i] = archivo[i] + resp.split('href="')[i].split('" class')[0]

	headers = {
	    'Authorization': 'Bearer '+BITLY_TOKEN,
	    'Content-Type': 'application/json',
	}

	data = '{ "long_url": "'+archivo[i]+'", "domain": "bit.ly"}'

	acortado = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
	open('link.json', 'w').write(acortado.text)
	f = open('link.json')
	json_file = json.load(f)
	json_str = json.dumps(json_file)
	resp2 = json.loads(json_str)
	archivo[i] = resp2 ["id"]

	tweet = "Vacunación masiva en "+lugares[i]+"\nℹ️ Más info: "+archivo[i]+"\n\n"
	api.update_status(tweet)

    
