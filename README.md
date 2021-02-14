# Python-based OpenHIM mediators(Docker) for OpenIMIS


The code contains Python-based OpenHIM mediators created for Healthix by **Dr. Stephen Mburu** and **Mr. Peter Kaniu.** The developers are based in School of Computing and Informatics, University of Nairobi. The mediators expose FHIR R4 APIs for exchange of data between openIMIS and external systems via openHIM.

---

# Installation Guide

This guide assumes successful installation of OpenIMIS (http://openimis.org/), OpenHIM (https://openhim.org), docker and docker-compose.

To run the mediator:

1. Git clone this repo - https://github.com/ahoazure/openhim_mediators_docker.git

    `git clone https://github.com/ahoazure/openhim_mediators_docker.git`
    
2. Cd into the repo openhim_mediators_docker

    `cd cd openhim_mediators_docker`
    
3. Run `docker-compose build`
4. Make migrations

    `docker-compose run mediators python manage.py  makemigrations`

5. Create Super User

    `docker-compose run mediators python manage.py  createsuperuser`
    
6. Login to the admin and update config variables
7. Go to the /mediators/urls.py file and uncomment the last block of code
8. Run `docker-compose up`
9. Confirm mediators have been successfully registered in the openhim console
