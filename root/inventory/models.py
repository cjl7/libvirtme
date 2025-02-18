from django.db import models

# Create your models here.
class PhysicalHost(models.Model):
    name = models.CharField(max_length=20)
    connection_string = models.CharField(max_length=80)