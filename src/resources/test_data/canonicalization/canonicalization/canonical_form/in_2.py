# Make series of nested if statements
# Delete the day variable, because it is a const
def get_day_number(day_of_week):
    day = 0
    if day_of_week == 'Monday':
        day = 1
        return day
    if day_of_week == 'Tuesday':
        day = 2
        return day
    if day_of_week == 'Wednesday':
        day = 3
        return day
    if day_of_week == 'Thursday':
        day = 4
        return day
    return day
