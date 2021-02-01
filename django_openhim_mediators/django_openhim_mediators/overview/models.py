

from django.db import models

# This model is used to facilitate changing URLs on admin
class configs(models.Model):
    openimis_url = models.CharField(max_length=200)
    openhim_url = models.CharField(max_length=200)
    mediator_url = models.CharField(max_length=200)

    openimis_port = models.IntegerField()
    openhim_port = models.IntegerField()
    mediator_port = models.IntegerField()


    def __str__(self):
        return self.openimis_url

    # Override Save method to store only one instance
    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)