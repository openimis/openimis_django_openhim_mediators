"""
Settings for openhim claim mediator developed in Django.

The python-based claim mediator implements python-utils 
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


@api_view(['GET', 'POST'])
def getClaims(request):
	# Query the upstream server via openHIM mediator port 8000
	# Caution: To secure the endpoint with SSL certificate,FQDN is required 
	if request.method == 'GET':
		url = "http://104.248.143.105:8000/api/api_fhir_r4/Claim"
		querystring = {"":""}
		payload = ""
		headers = {'Authorization': 'Basic aGVhbHRoaXg6b3BlbmltaXM='}
		response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
		datac = json.loads(response.text)
		return Response(datac)
	elif request.method == 'POST':
		url = "http://104.248.143.105:8000/api/api_fhir_r4/Claim/"
		querystring = {"":""}
		data = json.dumps(request.data)
		payload = data
		headers = {
			'Content-Type': "application/json",
			'Authorization': "Basic aGVhbHRoaXg6b3BlbmltaXM="
			}
		response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
		datac = json.loads(response.text)
		return Response(datac)


def registerClaimsMediator():
	API_URL = 'https://104.236.37.64:8080'
	USERNAME = 'root@openhim.org'
	PASSWORD = 'healthcloud7'

	result = configview()
	configurations = result.__dict__


	options = {
	'verify_cert': False,
	'apiURL': API_URL,
	'username': USERNAME,
	'password': PASSWORD,
	'force_config': False,
	'interval': 10,
	}

	conf = {
	"urn": "urn:mediator:python_fhir_r4_claim_mediator",
	"version": "1.0.1",
	"name": "Python Fhir R4 Claim Mediator",
	"description": "Python Fhir R4 Claim Mediator",

	"defaultChannelConfig": [
		{
			"name": "Python Fhir R4 Claim Mediator",
			"urlPattern": "^/api/api_fhir_r4/Claim$",
			"routes": [
				{
					"name": "Python Fhir R4 Claim Mediator Route",
					"host": configurations["data"]["mediator_url"],
					"path": "/api/api_fhir_r4/Claim",
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
			"path": "/api/api_fhir_r4/Claim",
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
