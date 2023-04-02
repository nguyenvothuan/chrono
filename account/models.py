from django.db import models
from boilerplate_app.models import User
from company.models import Company
from datetime import datetime
from time_entry.models import TimeEntry
# Create your models here.


class Account(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    manager = models.ForeignKey(
        'Account', on_delete=models.CASCADE, blank=True, default=None, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, default=None, null=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=True, null=True, default=None
    )
    positionTitle = models.CharField(max_length=100, blank=True, default="")
    startDate = models.DateField(default=datetime.now)
    isManager = models.BooleanField(default=False)
    
    def time_entries(self, start_date=None, end_date=None):
        qs = TimeEntry.objects.filter(account=self)
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        return qs