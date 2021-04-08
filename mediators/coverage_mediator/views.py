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
def getCoverage(request):
	result = configview()
	configurations = result.__dict__
	resp = requests.get(configurations["data"]["sosys_url"]+'/covers/get_covers/')
	data = resp.json()
	for coverage in data:
		requests.post(configurations["data"]["openimis_url"]+'Coverage/',auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]),json=coverage)
	return Response(data)
	
def registerCoverageMediator():
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
	"urn": "urn:mediator:python_fhir_r4_Coverage_mediator",
	"version": "1.0.1",
	"name": "Python Fhir R4 Coverage Mediator",
	"description": "Python Fhir R4 Coverage Mediator",

	"defaultChannelConfig": [
		{
			"name": "Python Fhir R4 Coverage Mediator",
			"urlPattern": "^/Coverage$",
			"routes": [
				{
					"name": "Python Fhir R4 Coverage Mediator Route",
					"host": configurations["data"]["mediator_url"],
					"path": "/Coverage",
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
			"name": "Python Fhir R4 Coverage Mediator Endpoint",
			"host": configurations["data"]["mediator_url"],
			"path": "/Coverage",
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
