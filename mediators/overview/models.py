"""
Model for making is earsier to change the base URls for openIMIS.
openHIM and the mediators.

The the upstream server urls for openHIM, openIMIS and mediators 
For more information on this file, contact the Python developers
Stephen Mburu:ahoazure@gmail.com & Peter Kaniu:peterkaniu254@gmail.com

"""

from django.db import models

# This model is used to facilitate changing URLs on admin
class configs(models.Model):
    openimis_url = models.URLField(max_length = 200,blank=True,null=True)
    openhim_url = models.URLField(max_length = 200,blank=True,null=True)
    sosys_url = models.URLField(max_length = 200,blank=True,null=True)
    openhim_user = models.CharField(max_length=200,blank=True,null=True)
    openhim_passkey = models.CharField(max_length=200,blank=True,null=True)
    openimis_user = models.CharField(max_length=200,blank=True,null=True)
    openimis_passkey = models.CharField(max_length=200,blank=True,null=True)
    openimis_port = models.IntegerField()
    openhim_port = models.IntegerField()
    mediator_url = models.CharField(max_length=200,blank=True,null=True)
    mediator_port = models.IntegerField()


    def __str__(self):
        return self.openimis_url

    # Override Save method to store only one instance
    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)