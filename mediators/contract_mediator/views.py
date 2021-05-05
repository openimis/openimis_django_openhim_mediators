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

@api_view(['GET', 'POST'])
def getContract(request):
	result = configview()
	configurations = result.__dict__
	resp = requests.get(configurations["data"]["sosys_url"]+'/covers/get_covers/')
	data = resp.json()
	if request.method == 'GET':
		for contract in data:
			requests.post(configurations["data"]["openimis_url"]+'Contract/',auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]),json=contract)
		return Response(data)
	elif request.method == 'POST':
		data = request.data
		resp = requests.post(configurations["data"]["openimis_url"]+'Contract/',auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]),json=data)
		return Response(resp.json())
	else:
		pass

	
def registerContractMediator():
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
	"urn": "urn:mediator:python_fhir_r4_Contract_mediator",
	"version": "1.0.1",
	"name": "Python Fhir R4 Contract Mediator",
	"description": "Python Fhir R4 Contract Mediator",

	"defaultChannelConfig": [
		{
			"name": "Python Fhir R4 Contract Mediator",
			"urlPattern": "^/Contract$",
			"routes": [
				{
					"name": "Python Fhir R4 Contract Mediator Route",
					"host": configurations["data"]["mediator_url"],
					"path": "/Contract",
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
			"name": "Python Fhir R4 Contract Mediator Endpoint",
			"host": configurations["data"]["mediator_url"],
			"path": "/Contract",
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
