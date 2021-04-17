#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import requests 
import json
from datetime import date, datetime
from datetime import timedelta
import cv2
import os
import unicodedata 

def remove_accents(text): 
	acentos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'Á': 'A', 'E': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
	for acen in acentos:
		if acen in text:
			text = text.replace(acen, acentos[acen])
	return text


CONSUMER_KEY= os.environ['CONSUMER_KEY_VACCINE']
CONSUMER_SECRET =os.environ['CONSUMER_SECRET_VACCINE']
ACCESS_TOKEN= os.environ['ACCESS_TOKEN_VACCINE']
ACCESS_TOKEN_SECRET =os.environ['ACCESS_TOKEN_SECRET_VACCINE']



today = date.today()
today = today - timedelta(days=1)


url = 'https://analisis.datosabiertos.jcyl.es/api/records/1.0/search/?dataset=vacunacion-covid-19-por-grupo-y-criterio&q=&sort=fecha&facet=fecha&rows=20&facet=provincia&facet=grupo_vacunacion&refine.provincia=Le%C3%B3n&refine.fecha='+str(today)
respuesta = requests.get(url)
print (url)
open('respuesta.json', 'wb').write(respuesta.content)
f = open('respuesta.json')
json_file = json.load(f)
json_str = json.dumps(json_file)
resp = json.loads(json_str)
rows = resp['nhits']

grupo = {}
dosis={}
ciclo = {}

posicion = 105
total = 0
image = cv2.imread('template.png')



for i in range (rows):
	print (i)
	if (resp['records'][i]['fields']['dosis_administradas_acumulado'] == 0):
		i = i+1
	else:
		grupo[i] = resp['records'][i]['fields']['grupo_vacunacion']
		dosis[i] = resp['records'][i]['fields']['dosis_administradas_acumulado']
		ciclo[i] = resp['records'][i]['fields']['personas_vacunadas_ciclo_completo_acumulado']
		cv2.putText(image, remove_accents(grupo[i]).upper(), (220, posicion), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
		cv2.putText(image, str(dosis[i]), (70, posicion), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
		posicion = posicion + 85 
		total = total + dosis[i]
		print ("\n\n"+str(grupo[i])+"\n"+str(dosis[i])+"\n"+str(ciclo[i]))

today = today.strftime("%d-%m-%Y")
cv2.putText(image, str(total), (1150, 580), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
cv2.putText(image, str(today), (1160, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.imwrite('output.png', image)




auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

api.update_with_media("output.png", "La vacunación contra la COVID-19 avanza en León. Estos son los datos acumulados a dia de hoy ("+str(today)+"). Más info en: https://bit.ly/2PLqzwk")