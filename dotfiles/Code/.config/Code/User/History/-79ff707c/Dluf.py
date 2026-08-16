def days_later(days):
    #Formats days into string
    if days == 1:
        return '(next day)'
    elif days > 1:
        return f'({days} days later)'
    return ''
    

def add_time(start_time, end_time, day=False):

    # constants
    HOURS_IN_ONE_DAY = 24
    HOURS_IN_HALF_DAY = 12
    WEEK_DAYS = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    days_later = 0
    hour, min = start_time.split(':')
    min, period = min.split(' ')
    end_time_hrs, end_time_mins = end_time.split(":")

    #Additing the time 
    calc_min = int(min) + int(end_time_mins)
    calc_hour = (calc_min // 60) + int(hour) + int(end_time_hrs)
    
    new_time = 0
    return new_time

'''
Need to have an effective system through which time 
can be added properly.
    thinking
    Does a 24 hour clock help ?
'''

#Answers
add_time('3:00 PM', '3:10')
# Returns: 6:10 PM

add_time('11:30 AM', '2:32', 'Monday')
# Returns: 2:02 PM, Monday

add_time('11:43 AM', '00:20')
# Returns: 12:03 PM

add_time('10:10 PM', '3:30')
# Returns: 1:40 AM (next day)

add_time('11:43 PM', '24:20', 'tueSday')
# Returns: 12:03 AM, Thursday (2 days later)

add_time('6:30 PM', '205:12')
# Returns: 7:42 AM (9 days later)