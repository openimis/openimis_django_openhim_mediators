
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import requests
from datetime import datetime
from openhim_mediator_utils.main import Main
from time import sleep
from overview.models import configs
from overview.views import configview
from requests.auth import HTTPBasicAuth
import math

@api_view(['GET', 'POST'])
def getOrganisation(request):
	deactactivateCompany()
	result = configview()
	configurations = result.__dict__
	resp = requests.get(configurations["data"]["sosys_url"]+'/covers/Organisation/')
	for item in resp.json()['results']:
		res = requests.get(configurations["data"]["openimis_url"]+'Organisation/',auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]),params={'code':item['code']})
		if res.json()['total'] == 0:
			requests.post(configurations["data"]["openimis_url"]+'Organisation/',auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]), json=item)
		else:
			obj = res.json()['entry'][0]['resource']
			if obj['email'] != item['email'] or obj['address'] != item['address'] or obj['phone'] != item['phone'] or  obj['fax'] != item['fax'] or obj['name'] != item['name'] or  obj['accountancy_account'] != item['accountancy_account']:
				requests.put(configurations["data"]["openimis_url"]+'Organisation/'+obj['id']+'/',auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]),json=item)
						
	return Response("Successfully finished")

def deactactivateCompany():
	result = configview()
	configurations = result.__dict__
	count = requests.get(configurations["data"]["openimis_url"]+'Organisation/',auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]))
	page_size = math.ceil(count.json()['total']/10)
	page_count = range(1,page_size+1)
	for page in page_count:
		res = requests.get(configurations["data"]["openimis_url"]+'Organisation/?page-offset='+str(page),auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]))
		for company in res.json()['entry']:
			resp = requests.get(configurations["data"]["sosys_url"]+'/covers/Organisation/',params={'code':company['resource']['code']})
			if len(resp.json()['results'])==0:
				print(company['resource']['id'])
				data = requests.delete(configurations["data"]["openimis_url"]+'Organisation/'+company['resource']['id']+'/',auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]))
				print(data.json())
			
def registerOrganisationMediator():
	result = configview()
	configurations = result.__dict__
 
	API_URL = configurations["data"]["openhim_url"]+':'+str(configurations["data"]["openhim_port"])
	USERNAME = configurations["data"]["openhim_user"]
	PASSWORD = configurations["data"]["openhim_passkey"]

	options = {
	'verify_cert': False,
	'apiURL': API_URL,
	'username': USERNAME,
	'password': PASSWORD,
	'force_config': False,
	'interval': 10,
	}

	conf = {
	"urn": "urn:mediator:python_fhir_r4_Organisation_mediator",
	"version": "1.0.1",
	"name": "Python Fhir R4 Organisation Mediator",
	"description": "Python Fhir R4 Organisation Mediator",

	"defaultChannelConfig": [
		{
			"name": "Python Fhir R4 Organisation Mediator",
			"urlPattern": "^/Organisation$",
			"routes": [
				{
					"name": "Python Fhir R4 Organisation Mediator Route",
					"host": configurations["data"]["mediator_url"],
					"path": "/Organisation",
					"port": configurations["data"]["mediator_port"],
					"primary": True,
					"type": "http"
				}
			],
			"allow": ["admin"],
			"methods": ["GET", "POST"],
			"type": "http"
		}
	],

	"endpoints": [
		{
			"name": "Python Fhir R4 Organisation Mediator Endpoint",
			"host": configurations["data"]["mediator_url"],
			"path": "/Organisation",
			"port": configurations["data"]["mediator_port"],
			"primary": True,
			"type": "http"
		}
	]
	}

	openhim_mediator_utils = Main(
		options=options,
		conf=conf
		)

	openhim_mediator_utils.register_mediator()
	checkHeartbeat(openhim_mediator_utils)



# Morning the health status of the client on the console
def checkHeartbeat(openhim_mediator_utils):
	openhim_mediator_utils.activate_heartbeat()
