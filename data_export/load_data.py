from account.models import Account
from boilerplate_app.models import User
from company.models import Company
import json
import datetime
with open("data_export/GizmoGram-employees.json") as f:
    employees = json.load(f)

for employee in employees:
    # create account
    try:
        account = Account.objects.create(
            id=employee.get("employeeId"),
            positionTitle=employee.get("positionTitle"),
            isManager=employee.get("isManager"),
            startDate=datetime.datetime.strptime(
                employee.get("startDate"), '%Y-%m-%d').date()
        )
    except:
        account = Account.objects.get(pk=employee.get("employeeId"))
    # search for company
    try:
        company = Company.objects.get(pk=employee.get("companyId"))
    except:
        company = Company.objects.create(id=employee.get(
            "companyId"), name=employee.get("companyName"))
    # create user

    # link account with user

    # link account with company
    break
