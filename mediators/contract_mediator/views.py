"""
Settings for openhim Contract mediator developed in Django.

The python-based Contract mediator implements python-utils 
from https://github.com/de-laz/openhim-mediator-utils-py.git.

For more information on this file, contact the Python developers
Stephen Mburu:ahoazure@gmail.com & Peter Kaniu:peterkaniu254@gmail.com

"""

from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import http.client

import json


import urllib3
import requests
from datetime import datetime
from openhim_mediator_utils.main import Main
from time import sleep

from overview.models import configs
from overview.views import configview
import http.client
import base64


@api_view(['GET', 'POST'])
def getContract(request):
	result = configview()
	configurations = result.__dict__
	authvars = configurations["data"]["openimis_user"]+":"+configurations["data"]["openimis_passkey"]#username:password-openhimclient:openhimclientPasskey
	# Standard Base64 Encoding
	encodedBytes = base64.b64encode(authvars.encode("utf-8"))
	encodedStr = str(encodedBytes, "utf-8")
	auth_openimis = "Basic " + encodedStr
	url = configurations["data"]["openimis_url"]+":"+str(configurations["data"]["openimis_port"])+"/api/api_fhir_r4/Contract"
	# Query the upstream server via openHIM mediator port 8000
	# Caution: To secure the endpoint with SSL certificate,FQDN is required 
	if request.method == 'GET':
		querystring = {"":""}
		payload = ""
		headers = {'Authorization': auth_openimis} 
		response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
		datac = json.loads(response.text)
		return Response(datac)
	elif request.method == 'POST':
		querystring = {"":""}
		data = json.dumps(request.data)
		payload = data
		headers = {
			'Content-Type': "application/json",
			'Authorization': auth_openimis
			}
		response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
		datac = json.loads(response.text)
		return Response(datac)


def registerContractMediator():
	result = configview()
	configurations = result.__dict__

	API_URL = 'https://'+configurations["data"]["openhim_url"]+':'+str(configurations["data"]["openhim_port"])
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
			"urlPattern": "^/api/api_fhir_r4/Contract$",
			"routes": [
				{
					"name": "Python Fhir R4 Contract Mediator Route",
					"host": configurations["data"]["mediator_url"],
					"path": "/api/api_fhir_r4/Contract",
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
			"name": "Bootstrap Scaffold Mediator Endpoint",
			"host": configurations["data"]["mediator_url"],
			"path": "/api/api_fhir_r4/Contract",
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
