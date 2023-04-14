from django.db import IntegrityError, transaction
from django.db.models import F
from account.models import Account
from boilerplate_app.models import User
from company.models import Company
from time_entry.models import TimeEntry
from data_export.util import get_company_employee_id, get_account_id, compute_hours_between_clock_times
import json
import datetime

# @transaction.atomic


def dump_employee():
    for file in ["Onion_Technology-employees", "GizmoGram-employees", "LunchRock_LLC-employees", "Night_Owls_Inc-employees"]:
        with open(f"data_export/{file}.json") as f:
            employees = json.load(f)

        for employee in employees:
            # create account
            userId = 10000*employee.get("companyId") + \
                employee.get("employeeId")
            try:
                account = Account.objects.create(
                    id=userId,
                    positionTitle=employee.get("positionTitle"),
                    isManager=employee.get("isManager"),
                    startDate=datetime.datetime.strptime(
                        employee.get("startDate"), '%Y-%m-%d').date()
                )
            except:
                account = Account.objects.get(pk=userId)
            # search for company
            try:
                company = Company.objects.get(pk=employee.get("companyId"))
            except:
                company = Company.objects.create(id=employee.get(
                    "companyId"), name=employee.get("companyName"))
                company.save()
            # create user
            try:
                user = User.objects.create(
                    # id=employee.get("employeeId"),
                    email=employee.get("email"),
                    username=employee.get("email").split("@")[0],
                    first_name=employee.get("firstName"),
                    last_name=employee.get("lastName"),
                    role=employee.get("positionTitle")
                )

            except:
                user = User.objects.get(email=employee.get("email"))
            # use encryption password scheme
            user.set_password(employee.get("password"))
            user.save()
            # link account with user
            print(user, account, company)
            account.user = user
            # link account with company
            account.company = company
            account.save()


@transaction.atomic
def dump_manager():
    for file in ["Onion_Technology-employees", "GizmoGram-employees", "LunchRock_LLC-employees", "Night_Owls_Inc-employees"]:
        with open(f"data_export/{file}.json") as f:
            employees = json.load(f)

        for employee in employees:
            # if the employee has a manager
            if 'managerId' in employee:
                userId = 10000*employee.get("companyId") + \
                    employee.get("employeeId")
                managerId = 10000*employee.get("companyId") + \
                    employee.get("managerId")
                user = Account.objects.get(pk=userId)
                manager = Account.objects.get(pk=managerId)
                user.manager = manager
                user.save()


@transaction.atomic
def dump_time_entries():
    for file in ["LunchRock_LLC", "Onion_Technology", "Night_Owls_Inc", "GizmoGram"]:
        with open(f"data_export/{file}-time-entries.json") as f:
            time_entries = json.load(f)
            companyId = 1
            if file == 'Onion_Technology':
                companyId = 1
            elif file == 'LunchRock_LLC':
                companyId = 2
            elif file == 'Night_Owls_Inc':
                companyId = 3
            else:
                companyId = 4
            for time_entry in time_entries:
                accountId = get_account_id(
                    company_id=companyId, employee_id=time_entry['employeeId'])
                account = Account.objects.get(pk=accountId)
                for entry in time_entry.get('timeEntries'):
                    # compute the hoursWorked here:
                    hoursWorked = 0
                    date = datetime.date.today()
                    if file == 'GizmoGram':
                        hoursWorked = entry.get('hoursWorked')
                        date = datetime.datetime.strptime(
                            entry.get("date"), '%Y-%m-%d').date()
                    elif file in ['LunchRock_LLC', 'Night_Owls_Inc']:
                        hoursWorked = compute_hours_between_clock_times(
                            entry.get('clockedIn'), entry.get('clockedOut'))
                        date = datetime.datetime.strptime(
                            entry.get("date"), '%Y-%m-%d').date()
                    elif file == 'Onion_Technology':
                        hoursWorked = compute_hours_between_clock_times(entry.get(
                            'clockedInEpochMillisecond'), entry.get('clockedOutEpochMillisecond'))
                        date = datetime.date.fromtimestamp(
                            entry.get('clockedInEpochMillisecond')/1000)
                    # handle case when there are two clock in clock out a day
                    try:
                        newEntry, created = TimeEntry.objects.get_or_create(
                            date=date, account=account, defaults={"hoursWorked": hoursWorked})
                        # data was created before, update the new time.
                        if not created:
                            newEntry.hoursWorked += F('hoursWorked') + \
                                hoursWorked
                            newEntry.save()
                    except IntegrityError as e:
                        print(account, date)
                        print(e)


def flush_time_entries():
    TimeEntry.objects.all().delete()


# dump_employee()
# dump_time_entries()
dump_manager()