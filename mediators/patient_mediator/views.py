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
from overview.models import configs
from overview.views import configview
from requests.auth import HTTPBasicAuth
import math

@api_view(['GET', 'POST'])
def getPatient(request):
	result = configview()
	configurations = result.__dict__
	resp = requests.get(configurations["data"]["sosys_url"]+'/members/memberlist/')
	for item in resp.json()['results']:
		for identifier in item['identifier']:
			if identifier['type']['coding'][0]['code'] == 'SB':
				res = requests.get(configurations["data"]["openimis_url"]+'Patient/',auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]),params={'identifier':identifier['value']})
				if res.json()['total'] == 0:
					requests.post(configurations["data"]["openimis_url"]+'Patient/',auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]), json=item)
				else:
					obj = res.json()['entry'][0]['resource']
					if obj['birthDate'] != item['birthDate'] or obj['telecom'] != item['telecom'] or  obj['name'] != item['name']:
						requests.put(configurations["data"]["openimis_url"]+'Patient/'+obj['id']+'/',auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]),json=item)
	return Response("Successfully synced patients")

def registerPatientMediator():
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
	"urn": "urn:mediator:python_fhir_r4_Patient_mediator",
	"version": "1.0.1",
	"name": "Python Fhir R4 Patient Mediator",
	"description": "Python Fhir R4 Patient Mediator",

	"defaultChannelConfig": [
		{
			"name": "Python Fhir R4 Patient Mediator",
			"urlPattern": "^/Patient$",
			"routes": [
				{
					"name": "Python Fhir R4 Patient Mediator Route",
					"host": configurations["data"]["mediator_url"],
					"path": "/Patient",
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
			"name": "Python Fhir R4 Patient  Mediator Endpoint",
			"host": configurations["data"]["mediator_url"],
			"path": "/Patient",
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
