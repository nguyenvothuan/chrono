from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from time_entry.models import TimeEntry
from account.utils import date_field_from_date
from datetime import datetime
# Create your views here.


class Punch(APIView):
    def post(self, request):
        try:
            user = request.user
            # print(user)
            # there is only one account for each user, and vice-versa
            account = user.account_set.first()
            now = datetime.now().time()
            today = datetime.today().date()
            time_entries = TimeEntry.objects.filter(account=account, date=today)
            if time_entries.count() == 0:
                # if a new day, create a new entry and start counting
                entry = TimeEntry.objects.create(date=today, hoursWorked=0, account=account, start_time=now)
            else:
                entry = time_entries.first()
                # if entry time is null, set it to the current time, start counting
                if entry.start_time == None:
                    entry.start_time = now
                # else, get the time difference from starttime and now, add that back to hoursWorked, apply with min function, then set starttime to null again/
                else:
                    difference = datetime.combine(datetime.today(), now) - datetime.combine(datetime.today(), entry.start_time)
                    hours_diff = difference.total_seconds() / 3600
                    print("Time since last punch in is : ", hours_diff)
                    hours_diff = round(hours_diff, 2)
                    entry.start_time = None
                    entry.hoursWorked = min(12, entry.hoursWorked + int(hours_diff))
            print(entry)
            entry.save()                
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class GetStartTime(APIView):
    def get(self, request):
        try:
            user = request.user
            account = user.account_set.first()
            today = datetime.today().date()
            time_entries = TimeEntry.objects.filter(account=account, date=today)

            if time_entries.count() == 0:
                return Response({'status': 'success', 'Response': {'start time': None}}, 
                                status=status.HTTP_200_OK)
            else:
                entry = time_entries.first()
                if entry.start_time == None:
                    return Response({'status': 'success', 'Response': {'start time': None}}, 
                                status=status.HTTP_200_OK)
                else:
                    time = entry.start_time
                    return Response({'status': 'success', 'Response': {'start time': time}}, 
                                status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)