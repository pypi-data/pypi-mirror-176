import datetime
from datetime import datetime

def calc_age(dob: str, unit: str) -> str:
    """ 
    Given a date of birth, returns a conversion based on the unit desired. 

    The format of the dob should be %b %d %Y %I:%M%p (e.g., Jan 10 2000 12:00AM).

    Note: This function may or may not account for leap years.
    """

    try:
        my_dob = datetime.strptime(str(dob), "%b %d %Y %I:%M%p")
    except ValueError:
        raise Exception("Invalid date format")

    today = datetime.now()
    days30 = {4, 6, 9, 11}
    days31 = {1, 3, 5, 7, 8, 10, 12}
    timedelta = today - my_dob
    days = timedelta.days
    weeks = timedelta.days // 7
    hours = timedelta.seconds // 3600 + days * 24
    minutes = timedelta.seconds // 60 + hours * 60
    seconds = timedelta.seconds + minutes * 60

    if (my_dob.month > today.month):
        curr_years = today.year-my_dob.year-1
        curr_months = abs(my_dob.month - (12 - today.month))
    else:
        curr_years = today.year-my_dob.year
        curr_months = today.month-my_dob.month
    if (my_dob.day > today.day):
        curr_months = curr_months - 1
    if (my_dob.month in days30):
        curr_days = abs((30 - my_dob.day) + today.day)
    elif (my_dob.month in days31):
        curr_days = abs((31 - my_dob.day) + today.day)
    else:
        curr_days = abs((28 - my_dob.day) + today.day)
    # zero out the time portion of the datetime object
    if(curr_months<1):
        temp_months = 1
        curr_months = 1
    else:
        temp_months = 0
    # 
    if(curr_years<1):
        temp_years = 1
        curr_years = 1
    else:
        temp_years = 0
    # 
    if(curr_days<1):
        temp_days = 1
        curr_days = 1
    else:
        temp_days = 0
        
    # curr_= datetime(curr_years, curr_months, curr_days)

    months = curr_years * 12 + curr_months

    if unit == "actual":
        return str(curr_years - temp_years) + " years " + str(curr_months - temp_months) + " months and " + str(curr_days - temp_days) + " days old"
    elif unit == "years":
        return str(curr_years - temp_years) + " years old"
    elif unit == "months":
        return str(months - temp_months) + " months old"
    elif unit == "weeks":
        return str(weeks) + " weeks old"
    elif unit == "days":
        return str(days) + " days old"
    elif unit == "hours":
        return str(hours) + " hours old"
    elif unit == "minutes":
        return str(minutes) + " minutes old"
    elif unit == "seconds":
        return str(seconds) + " seconds old"
    else:
        return "Invalid input"


def help():
    """
    Provides some help with using the calc_age function.
    """
    print("calc_age(dob, unit):")
    print("\tInput dob in the following format: MTH DAY YEAR TIME")
    print("\tThese are the available units to convert into:", __units())
    print("\tExample:")
    print("\t\t>> calc_age('Jan 1 2000 1:33PM', 'years')")
    print("\t\t" + calc_age('Jan 1 2000 1:33PM', 'years'))


def __units():
    """
    Used to store the valid units of conversions.
    """
    return ['actual', 'years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds']

# def main():
#     years = [2001, 2010, 2021]
#     months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#     days = [i for i in range(1, 28)]
#     times = ["12:00AM", "5:43PM", "11:30AM", "2:00PM", "7:20PM"]
#     units = ['actual', 'years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds']
#     try:
#         for year in years:
#             for month in months:
#                 for day in days:
#                     for time in times:
#                         for unit in units:
#                             dob = " ".join([month, str(day), str(year), time])
#                             calc_age(dob, unit)
                            
#     except ValueError as e:
#         assert False, f"ValueError: {e.args[0]} ({dob} {unit})"
#     except Exception as e:
#         assert False, f"Exception: {e.args[0]} ({dob} {unit})"
#     assert True
# main()