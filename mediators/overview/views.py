
from django.shortcuts import render
from dotenv import dotenv_values
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import http.client
from .models import configs
from .serializers import configsSerializer

def congifgurations():
    config_info= dotenv_values('.env')
    configs.objects.all().delete()
    configs.objects.create(**config_info)
    
def configview():
	config = configs.objects.first()
	serializer = configsSerializer(config, many = False)
	return Response(serializer.data)