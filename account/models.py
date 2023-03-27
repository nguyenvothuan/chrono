from django.db import models
from boilerplate_app.models import User
from datetime import datetime
# Create your models here.
class Account(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    manager = models.ForeignKey('Account', on_delete=models.CASCADE, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=True)
    positionTitle = models.CharField(max_length=100, blank=True, default="")
    startDate = models.DateField(default=datetime.now())
    isManager = models.BooleanField(default=False)
    
