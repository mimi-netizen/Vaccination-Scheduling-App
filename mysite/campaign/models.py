from django.db import models
from center.models import Center
from vaccine.models import Vaccine
from django.contrib.auth import get_user_model

User = get_user_model()

class Campaign(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    agents = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return str(self.vaccine.name).upper() + " | " + str(self.center.name).upper()


class Slot(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    max_capacity = models.IntegerField(default=0, null=True, blank=True)
    reserved = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.date) + " | " + str(self.start_time) + " to " + str(self.end_time)
