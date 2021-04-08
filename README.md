# Python-based OpenHIM mediators(Docker) for OpenIMIS


The code contains Python-based OpenHIM mediators created for Healthix. The mediators expose FHIR R4 APIs for exchange of data between openIMIS and external systems via openHIM.

---

# Installation Guide
This guide assumes successful installation of OpenIMIS (http://openimis.org/), docker and docker-compose.

To run the mediator:

1. Requirements - docker-compose.yml file - https://github.com/openimis/openimis_django_openhim_mediators/blob/master/docker-compose.yml
    
2. Run `docker-compose up -d`


3. Create Super User

    `docker-compose run mediators python manage.py  createsuperuser`
    
4. Login to the admin and update config variables
   NB: remember to delete default superuser

5. Confirm mediators have been successfully registered in the openhim console

NB: For standalone installation of openHIM see http://openhim.org/docs/getting-started/install