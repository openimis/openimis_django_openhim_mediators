"""
View for registering endpoint serializers on DRF

The the upstreame server urls for openhim, openimis 
and python mediators 
For more information on this file, contact the developers
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

# This seriializer uses the configs model 
from .models import configs
from .serializers import configsSerializer

# Method to restrict serializer to only one instance
def configview():
	config = configs.objects.first()
	serializer = configsSerializer(config, many = False)
	return Response(serializer.data)