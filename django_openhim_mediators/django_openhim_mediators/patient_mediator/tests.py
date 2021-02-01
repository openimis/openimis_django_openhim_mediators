from django.test import TestCase

# Create your tests here.
import http.client

conn = http.client.HTTPConnection("104.236.37.64:5001")

payload = " "#you payload goes here

headers = {
    'Authorization': "Basic aGVhbHRoMTpoZWFsdGhAMTIz",
    'Content-Type': "application/json"
    }

conn.request("POST", "/api/api_fhir_r4/Organisation", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))