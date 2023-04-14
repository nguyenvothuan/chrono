from datetime import datetime, timedelta
def get_company_employee_id(id):
    res = {}
    res['company_id'] = id % 10000
    res['employee_id'] = id % 10000
    return res


def get_account_id(company_id, employee_id):
    return 10000*company_id+employee_id


def compute_hours_between_clock_times(clocked_in, clocked_out):
    if isinstance(clocked_in, int) and isinstance(clocked_out, int):
        clocked_in = datetime.fromtimestamp(clocked_in / 1000.0).strftime('%H:%M:%S')
        clocked_out = datetime.fromtimestamp(clocked_out / 1000.0).strftime('%H:%M:%S')
    elif not isinstance(clocked_in, str) or not isinstance(clocked_out, str):
        raise ValueError("Input times must be either strings or epoch times")
    
    clocked_in_time = datetime.strptime(clocked_in, '%H:%M:%S')
    clocked_out_time = datetime.strptime(clocked_out, '%H:%M:%S')
    hours_worked = clocked_out_time - clocked_in_time
    return round(hours_worked.total_seconds() / 3600.0, 2)

