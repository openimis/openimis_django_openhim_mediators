"""
Settings for openhim Patient mediator developed in Django.

The python-based Patient mediator implements python-utils 
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
def getPortPart(p):

	if(p=="" or p=="80" or p==80):
		return ""

	return ":"+str(p)

@api_view(['POST'])
def savePrefs(request):
	requestt = {
		"method":'GET'
	}
	# getPatient(requestt)

	org_id = request.data.get("id")
	# host = request.data.get("id")
	# username = request.data.get("id")
	# password = request.data.get("id")

	# return Response({"org_id":org_id})

	result = configview()
	configurations = result.__dict__
	
	print("Step 1")


	authvars_him = configurations["data"]["openhim_user"]+":"+configurations["data"]["openhim_passkey"]#username:password-openhimclient:openhimclientPasskey
	# Standard Base64 Encoding
	encodedBytes_home = base64.b64encode(authvars_him.encode("utf-8"))
	encodedStr_him = str(encodedBytes_home, "utf-8")
	auth_openhim = "Basic " + encodedStr_him
	# /api/api_fhir_r4/Patient

	url_him_get = configurations["data"]["openhim_url"]+":"+str(5001)+"/api/api_fhir_r4/Patient"
	url_him = configurations["data"]["openhim_url"]+":"+str(5001)+"/api/lafia/PatientResource"


	print("Step 2")
	querystring = {"":""}
	payload = ""
	# headers = {'Authorization': auth_openhim}
	headers = {'Content-Type': "application/json"}
	print(url_him_get)
	print(headers)
	response = requests.request("GET", url_him_get, data=payload, headers=headers, params=querystring)
	print("Step 2.1")
	print(response.status_code)
	datac = json.loads(response.text)

	print("Step 3")

	datac["type"] = "transaction"

	request_dict = {
		"request": {
			"method": "POST"
		}
	}

	org = {
		"managingOrganization": {
			"reference": "Organization/"+str(org_id)
		}
	}



	for i in range(len(datac["entry"])):
		datac["entry"][i].update(request_dict)
		datac["entry"][i]["resource"].update(org)

	data = json.dumps(datac)
	print(data)
	payload = data
	headers = {
		'Content-Type': "application/json",
		# 'Authorization': auth_openhim
		}
	responsee = requests.request("POST", url_him, data=payload, headers=headers, params=querystring)
	print("Step 3.1")
	print(url_him)
	print(responsee.status_code)
	# datac = json.loads(responsee.text)

	print("Step 4")
	return Response({"nooo":"yes"})




	# call getter openhim
	# call poster

	return Response({"ok":"thankyou"})
@api_view(['GET', 'POST'])
def getPatient(request):
	print(" yes I was here 3")
	
	result = configview()
	configurations = result.__dict__
	authvars = configurations["data"]["openimis_user"]+":"+configurations["data"]["openimis_passkey"]#username:password-openhimclient:openhimclientPasskey
	# Standard Base64 Encoding
	encodedBytes = base64.b64encode(authvars.encode("utf-8"))
	encodedStr = str(encodedBytes, "utf-8")
	auth_openimis = "Basic " + encodedStr



	# Standard Base64 Encoding
	url = configurations["data"]["openimis_url"]+getPortPart(configurations["data"]["openimis_port"])+"/api/api_fhir_r4/Patient"
	# Query the upstream server via openHIM mediator port 8000
	# Caution: To secure the endpoint with SSL certificate,FQDN is required 
	if request.method == 'GET':
		print(" yes I was here")
		querystring = {"":""}
		payload = ""
		headers = {'Authorization': auth_openimis}
		print(url)
		print(headers)
		response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
		datac = json.loads(response.text)


		return Response(datac)
	elif request.method == 'POST':
		print(" yes I was here 2")

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


def registerPatientMediator():
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
	"urn": "urn:mediator:python_fhir_r4_Patient_mediator",
	"version": "1.0.1",
	"name": "Python Fhir R4 Patient Mediator",
	"description": "Python Fhir R4 Patient Mediator",

	"defaultChannelConfig": [
		{
			"name": "Python Fhir R4 Patient Mediator",
			"urlPattern": "^/api/api_fhir_r4/Patient$",
			"routes": [
				{
					"name": "Python Fhir R4 Patient Mediator Route",
					"host": configurations["data"]["mediator_url"],
					"path": "/api/api_fhir_r4/Patient",
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
			"path": "/api/api_fhir_r4/Patient",
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
