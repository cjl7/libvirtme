from django.db import models

# Create your models here.
class PhysicalHost(models.Model):
    name = models.CharField(max_length=20, unique=True)
    connection_string = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class VirtualHost(models.Model):
    name = models.CharField(max_length=40, unique=True)
    physical_host = models.ForeignKey(PhysicalHost, on_delete=models.CASCADE)
    state = models.IntegerField()
    memory = models.IntegerField()
    vcpus = models.IntegerField()
    disk = models.IntegerField()
    disk_used = models.IntegerField(default=0)

    def __str__(self):
        return self.name
