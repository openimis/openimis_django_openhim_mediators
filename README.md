# Python-based OpenHIM mediators(Docker) for OpenIMIS


The code contains Python-based OpenHIM mediators created for Healthix by **Dr. Stephen Mburu** and **Mr. Peter Kaniu.** The developers are based in School of Computing and Informatics, University of Nairobi. The mediators expose FHIR R4 APIs for exchange of data between openIMIS and external systems via openHIM.

---

# Installation Guide

This assumes successful installation of OpenIMIS (http://openimis.org/), OpenHIM (https://openhim.org) docker and docker-compose, .

Some reasons you might want to use REST framework:

* The [Web browsable API][sandbox] is a huge usability win for your developers.
* [Authentication policies][authentication] including optional packages for [OAuth1a][oauth1-section] and [OAuth2][oauth2-section].
* [Serialization][serializers] that supports both [ORM][modelserializer-section] and [non-ORM][serializer-section] data sources.
* Customizable all the way down - just use [regular function-based views][functionview-section] if you don't need the [more][generic-views] [powerful][viewsets] [features][routers].
* [Extensive documentation][docs], and [great community support][group].

