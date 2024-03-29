from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from time_entry.models import TimeEntry
from account.models import Account
from account.utils import date_field_from_date
from datetime import datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
# Create your views here.


class Punch(APIView):
    def post(self, request):
        try:
            user = request.user
            # there is only one account for each user, and vice-versa
            account = user.account_set.first()
            now = datetime.now().time()
            today = datetime.today().date()
            time_entries = TimeEntry.objects.filter(
                account=account, date=today)
            if time_entries.count() == 0:
                # if a new day, create a new entry and start counting
                entry = TimeEntry.objects.create(
                    date=today, hoursWorked=0, account=account, start_time=now)
            else:
                entry = time_entries.first()
                # if entry time is null, set it to the current time, start counting
                if entry.start_time == None:
                    entry.start_time = now
                # else, get the time difference from starttime and now, add that back to hoursWorked, apply with min function, then set starttime to null again/
                else:
                    difference = datetime.combine(
                        datetime.today(), now) - datetime.combine(datetime.today(), entry.start_time)
                    hours_diff = difference.total_seconds() / 3600
                    print("Time since last punch in is : ", hours_diff)
                    hours_diff = round(hours_diff, 2)
                    entry.start_time = None
                    entry.hoursWorked = min(
                        12, entry.hoursWorked + int(hours_diff))
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
            time_entries = TimeEntry.objects.filter(
                account=account, date=today)

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

class HoursWorked(APIView):
    date = openapi.Parameter('date', in_=openapi.IN_QUERY,
                         type=openapi.TYPE_STRING)
    from_date = openapi.Parameter('from_date', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING)
    to_date = openapi.Parameter('to_date', in_=openapi.IN_QUERY,
                            type=openapi.TYPE_STRING)
    @swagger_auto_schema(
        manual_parameters=[date, from_date, to_date],
    )
    def get(self, request):
        try:
            user = request.user
            account = user.account_set.first()
            date = request.GET.get('date')
            from_date = request.GET.get('from_date')
            to_date = request.GET.get('to_date')
            if from_date != None and to_date != None:
                time_entries = TimeEntry.objects.filter(
                    account=account, date__range=[from_date, to_date])
                if time_entries == None:
                    return Response({'status': False, 'message': "No time entries for this user"},
                                    status=status.HTTP_400_BAD_REQUEST)
                results = []
                for time_entry in time_entries:
                    results.append(
                        {"Date": time_entry.date, "Hours": time_entry.hoursWorked})
                return Response({'status': 'success', 'Response': results}, status=status.HTTP_200_OK)
            elif date != None:
                time_entries = TimeEntry.objects.filter(
                    account=account, date=date)
                entry = time_entries.first()
                if entry == None:
                    return Response({'status': False, 'message': "No time entry for the specific date"},
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response({"Date": date, "Hours": entry.hoursWorked}, status=status.HTTP_200_OK)
            else:
                time_entries = TimeEntry.objects.filter(account=account)[:20]
                if time_entries == None:
                    return Response({'status': False, 'message': "No time entries for this user"},
                                    status=status.HTTP_400_BAD_REQUEST)
                results = []
                for time_entry in time_entries:
                    results.append(
                        {"Date": time_entry.date, "Hours": time_entry.hoursWorked})

                return Response({'status': 'success', 'Response': results}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        
class Me(APIView):
    def get(self, request):
        try:
            user = request.user
            account = user.account_set.first()
            company = account.company.name
            hasManager = account.manager
            if(hasManager != None):
                manager = account.manager.user.first_name + ' ' + account.manager.user.last_name
            else:
                manager = None
            email = user.email
            first_name = user.first_name
            last_name = user.last_name

            return Response({'status': 'success', 'Response': {'email':email, 'first_name':first_name, 'last_name':last_name, 'company':company, 'manager':manager}}, 
                                status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class EmployeeInfo:
    def __init__(self, email, first_name, last_name, company):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.company = company

class EmployeeInfoSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    company = serializers.CharField()

class GetEmployeeInfo(APIView):
    employee_id = openapi.Parameter('id', in_=openapi.IN_QUERY,
                         type=openapi.TYPE_STRING)   
    @swagger_auto_schema(
        manual_parameters=[employee_id],
    )
    def get(self, request):
        try:
            user = request.user
            account = user.account_set.first()
            manager_id = account.id

            employee_id = request.GET.get('id')
            if employee_id != None:
                employee_accounts = Account.objects.filter(id=employee_id)
                if len(employee_accounts) == 0:
                    return Response({'status': False, 'message': "Invalid employee id"},
                                    status=status.HTTP_403_FORBIDDEN)
                employee_account = employee_accounts[0]

                if employee_account.manager == None or employee_account.manager.id != manager_id:
                    return Response({'status': False, 'message': "Data is forbidden"},
                                    status=status.HTTP_403_FORBIDDEN)
                employeeInfo = EmployeeInfo(employee_account.user.email, employee_account.user.first_name, employee_account.user.last_name, employee_account.company.name)
                serializer = EmployeeInfoSerializer(employeeInfo)
                return Response({'status': 'success', 'Response': serializer.data}, 
                                status=status.HTTP_200_OK)
                
            employees = Account.objects.filter(manager=account)[:20]
            if employees == None:
                    return Response({'status': False, 'message': "No employees for this user"},
                                    status=status.HTTP_403_FORBIDDEN)
            results = []
            for employee in employees:
                    employeeInfo = EmployeeInfo(employee.user.email, employee.user.first_name, employee.user.last_name, employee.company.name)
                    serializer = EmployeeInfoSerializer(employeeInfo)
                    results.append(
                        serializer.data)

            return Response({'status': 'success', 'Response': results}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
                            

class EditEmployeeWorkHour(APIView):
    Input_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'date': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'hoursWorked': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    },
    required=['date', 'hoursWorked']
    )

    employee_id = openapi.Parameter('id', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)   
    @swagger_auto_schema(manual_parameters=[employee_id], request_body=Input_schema)
    def post(self, request):
        try:
            user = request.user
            account = user.account_set.first()
            manager_id = account.id
            newHoursWorked = request.data['hoursWorked']
            date = request.data['date']
            if newHoursWorked == None or date == None:
                return Response({'status': False, 'message': "Invalid Input"}, status=status.HTTP_400_BAD_REQUEST)

            employee_id = request.GET.get('id')
            print(employee_id)
            employee_accounts = Account.objects.filter(id=employee_id)
            if len(employee_accounts) == 0:
                return Response({'status': False, 'message': "Invalid employee id"}, status=status.HTTP_403_FORBIDDEN)

            employee_account = employee_accounts[0]
            if employee_account.manager == None or employee_account.manager.id != manager_id:
                return Response({'status': False, 'message': "Data is forbidden"}, status=status.HTTP_403_FORBIDDEN)

            time_entry = TimeEntry.objects.filter(account=employee_account, date=date).first()
            if time_entry == None:
                return Response({'status': False, 'message': "No time entry for the specific date"}, status=status.HTTP_400_BAD_REQUEST)

            time_entry.hoursWorked = newHoursWorked
            time_entry.save()

            return Response({'status': 'success'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetEmployeeWorkHour(APIView):
    employee_email = openapi.Parameter('employee_email', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)   
    date = openapi.Parameter('date', in_=openapi.IN_QUERY,
                         type=openapi.TYPE_STRING)
    from_date = openapi.Parameter('from_date', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING)
    to_date = openapi.Parameter('to_date', in_=openapi.IN_QUERY,
                            type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[employee_email, date, from_date, to_date])
    def get(self, request):
        try:
            user = request.user
            account = user.account_set.first()
            date = request.GET.get('date')
            from_date = request.GET.get('from_date')
            to_date = request.GET.get('to_date')
            email = request.GET.get('employee_email')
            employee = Account.objects.filter(user__email=email).first()
            print(employee)
            if employee.manager != account:
                return Response({'status': False, 'message': "Data is forbidden"}, status=status.HTTP_403_FORBIDDEN)
            #return the employee's time entries from date to date
            if from_date != None and to_date != None:
                time_entries = TimeEntry.objects.filter(
                    account=employee, date__range=[from_date, to_date])
                if time_entries == None:
                    return Response({'status': False, 'message': "No time entries for this user"},
                                    status=status.HTTP_400_BAD_REQUEST)
                results = []
                for time_entry in time_entries:
                    results.append(
                        {"Date": time_entry.date, "Hours": time_entry.hoursWorked})
                return Response({'status': 'success', 'Response': results}, status=status.HTTP_200_OK)
            elif date != None:
                time_entries = TimeEntry.objects.filter(
                    account=employee, date=date)
                entry = time_entries.first()
                if entry == None:
                    return Response({'status': False, 'message': "No time entry for the specific date"},
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response({"Date": date, "Hours": entry.hoursWorked}, status=status.HTTP_200_OK)
            else:
                time_entries = TimeEntry.objects.filter(account=employee)[:20]
                if time_entries == None:
                    return Response({'status': False, 'message': "No time entries for this user"},
                                    status=status.HTTP_400_BAD_REQUEST)
                results = []
                for time_entry in time_entries:
                    results.append(
                        {"Date": time_entry.date, "Hours": time_entry.hoursWorked})

                return Response({'status': 'success', 'Response': results}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
                            
    
    