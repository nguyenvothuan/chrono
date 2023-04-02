from django.db import models

# Create your models here.
class Company(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    name = models.CharField(max_length=50, blank=True, default="")
