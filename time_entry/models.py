from django.db import models
from datetime import datetime
# Create your models here.
class TimeEntry(models.Model):
    date=models.DateField(default=datetime.now)
    hoursWorked=models.DecimalField(decimal_places=2, max_digits=4)
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)