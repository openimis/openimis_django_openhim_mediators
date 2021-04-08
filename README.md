# Python-based OpenHIM mediators(Docker) for OpenIMIS


The code contains Python-based OpenHIM mediators created for Healthix. The mediators expose FHIR R4 APIs for exchange of data between openIMIS and external systems via openHIM.

---

# Installation Guide
This guide assumes successful installation of docker and docker-compose,openHIM Console and openHIM core-js (http://openhim.org/docs/installation/docker).


### OPENHIM CONFIGURATION

* create a `mediators/.env` file to provide your mediator  connection to openHIM:
```sh
openimis_url=http://104.248.143.105:8000/api/api_fhir_r4/  //specify openimis link to fhir 4 resources
openhim_url=https://104.236.60.156  // replace with link to the server hosting openHIM instance
sosys_url=http://165.22.141.60:3200 // replace with link to the third party system
openhim_user=root@openhim.org      // replace with  openHIM user
openhim_passkey=febvih-kIrfyz-gocje3 // replace with openHIM user passwoord
openimis_user=healthix   // replace with openimis technical user
openimis_passkey=openimis // replace with openimis technical user password
openimis_port=8000   
openhim_port=8080
mediator_url=104.236.60.156  // repalce with link to the server hosting openHIM
mediator_port=8000 // specify the mediator port  which is always the same with the mediators port
```
### Docker

To run the mediators navigate to the project directory  and run the following commands:

To run the mediator:

1. Requirements - docker-compose.yml file - https://github.com/openimis/openimis_django_openhim_mediators/blob/master/docker-compose.yml
    
2. Run `docker-compose build --no-cache && docker-compose up -d`

3. Create Super User

    `docker-compose run mediators python manage.py  createsuperuser`
    
4. Login to the admin and update config variables if you would like to update the configurations you had specified in the  `mediators/.env`
   NB: remember to delete default superuser

5. Confirm mediators have been successfully registered in the openhim console

NB: For standalone installation of openHIM see http://openhim.org/docs/getting-started/install