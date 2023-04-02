from account.models import Account
from boilerplate_app.models import User
from company.models import Company
import json
import datetime

for file in ["Onion_Technology-employees", "GizmoGram-employees", "LunchRock_LLC-employees", "Night_Owls_Inc-employees"]:
    with open(f"data_export/{file}.json") as f:
        employees = json.load(f)

    for employee in employees:
        # create account
        userId = 10000*employee.get("companyId") + employee.get("employeeId")
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
 