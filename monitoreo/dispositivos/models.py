from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, help_text="Zone description.")

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=100)
    power_consumption = models.IntegerField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Measurement(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    consumption_w = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Measurement for {self.device.name} - {self.consumption_w}W"

class Alert(models.Model):
    measurement = models.OneToOneField(Measurement, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    reviewed = models.BooleanField(default=False, help_text="Indicates if the alert has been reviewed.")

    def __str__(self):
        return f"Alert for {self.measurement.device.name}"

class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

    def __str__(self):
        return self.name