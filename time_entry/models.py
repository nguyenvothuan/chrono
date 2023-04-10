from django.db import models
from datetime import datetime
# Create your models here.
class TimeEntry(models.Model):
    date=models.DateField(default=datetime.now)
    #test update
    punchInTime = models.TimeField(default=datetime.now)
    punchOutTime = models.TimeField(default=datetime.now)
    #test update end
    hoursWorked=models.DecimalField(decimal_places=2, max_digits=4, default=0)
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    
    class Meta:
        #one account can only have 1 time_entry of a given date.
        unique_together = ('account', 'date')
        