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
import requests
from requests.auth import HTTPBasicAuth

@api_view(['GET', 'POST'])
def getClaimResponse(request):
	result = configview()
	configurations = result.__dict__
	data = requests.get(configurations["data"]["openimis_url"]+'ClaimResponse/',auth=HTTPBasicAuth(configurations["data"]["openimis_user"],configurations["data"]["openimis_passkey"]))
	res=data.json()
	requests.post(configurations["data"]["sosys_url"]+'/claims/valuated/',json=res['entry'])
	return Response(res)
	# if data.status_code == 200:
	# 	res=data.json()
	# 	print(res)
	# 	resp=requests.post(configurations["data"]["sosys_url"]+'/claims/valuated/',json=res['entry'])
	# 	return Response(res)
	# else:
	# 	return Response({"Error":"Failed to connect to openimis server with error code {}".format(data.status_code)})
	
def registerClaimResponseMediator():
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
	"urn": "urn:mediator:python_fhir_r4_ClaimResponse_mediator",
	"version": "1.0.1",
	"name": "Python Fhir R4 ClaimResponse Mediator",
	"description": "Python Fhir R4 ClaimResponse  Mediator",

	"defaultChannelConfig": [
		{
			"name": "Python Fhir R4 ClaimResponse Mediator",
			"urlPattern": "^/ClaimResponse$",
			"routes": [
				{
					"name": "Python Fhir R4 ClaimResponse Mediator Route",
					"host":configurations["data"]["mediator_url"],
					"path": "/ClaimResponse",
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
			"name": "Python ClaimResponse Mediator",
			"host":configurations["data"]["mediator_url"],
			"path": "/ClaimResponse",
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
def checkHeartbeat(openhim_mediator_utils):
	openhim_mediator_utils.activate_heartbeat()
