#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Python imports.
import logging

# Django imports.
from django.urls import path, re_path

# Rest Framework imports.

# Third Party Library imports

# local imports.
from account.views import Punch, GetStartTime, HoursWorked, Me, EditEmployeeWorkHour, GetEmployeeInfo, GetEmployeeWorkHour

app_name = 'accounts'

urlpatterns = [
    path('punch', Punch.as_view(), name='punch in punch out'), 
    path('hoursWorked', HoursWorked.as_view(), name='hours worked'),
    path('punch-in-time', GetStartTime.as_view(), name = "get punch in time"),
    path('me', Me.as_view(), name = "get user information"),
    path('manager/employees/id', EditEmployeeWorkHour.as_view(), name = "edit employee info"),
    path('manager/employees', GetEmployeeInfo.as_view(), name = "get employee info"),
    path('manager/employees/hoursWorked', GetEmployeeWorkHour.as_view(), name = "get employee info"),
    
]
