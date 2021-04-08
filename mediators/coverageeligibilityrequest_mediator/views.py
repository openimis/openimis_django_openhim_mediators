
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


@api_view(['POST'])
def getCoverageEligibilityRequest(request):
	result = configview()
	configurations = result.__dict__
	data = request.data
	resp = requests.post(configurations["data"]["sosys_url"]+'/members/eligibility/',json=data)	
	if resp.status_code == 200:
		return Response(resp.json())
	else:
		return  Response({"Error":"CoverageEligibility request failed {}".format(resp.status_code)})

def registerCoverageEligibilityRequestMediator():
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
	"urn": "urn:mediator:python_fhir_r4_CoverageEligibilityRequest_mediator",
	"version": "1.0.1",
	"name": "Python Fhir R4 CoverageEligibilityRequest Mediator",
	"description": "Python Fhir R4 CoverageEligibilityRequest Mediator",

	"defaultChannelConfig": [
		{
			"name": "Python Fhir R4 CoverageEligibilityRequest Mediator",
			"urlPattern": "^/CoverageEligibilityRequest$",
			"routes": [
				{
					"name": "Python Fhir R4 CoverageEligibilityRequest Mediator Route",
					"host": configurations["data"]["mediator_url"],
					"path": "/CoverageEligibilityRequest",
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
			"name": "Python Fhir R4 CoverageEligibilityRequest",
			"host": configurations["data"]["mediator_url"],
			"path": "/CoverageEligibilityRequest",
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
