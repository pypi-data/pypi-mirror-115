from time import time
from firstimpression.constants import APIS
from firstimpression.file import update_directories_api
from firstimpression.scala import variables
import datetime
##################################################################################################
# CONSTANTS
##################################################################################################

NAME = APIS['countdown']


##################################################################################################
# MAIN FUNCTIONS API
##################################################################################################

def check_api(end_year, end_month, end_day, end_hour, end_minute, end_second):
    update_directories_api(NAME)
    svars = variables()
    end_date = datetime.datetime(end_year, end_month, end_day, end_hour, end_minute, end_second)
    current_date = datetime.datetime.now()

    if current_date > end_date:
        pass
        svars['skipscript'] = True
    else:
        svars['skipscript'] = False
        time_delta = end_date - current_date
        
        days_remaining = time_delta.days
        years_remaining = days_remaining//365
        days_remaining -= years_remaining * 365
        weeks_remaining = days_remaining//7
        days_remaining -= weeks_remaining * 7

        seconds_remaining = time_delta.seconds
        hours_remaining = seconds_remaining//3600
        seconds_remaining -= hours_remaining * 3600
        minutes_remaining = seconds_remaining//60
        seconds_remaining -= minutes_remaining * 60

        svars['remaining_year'] = years_remaining
        svars['remaining_week'] = weeks_remaining
        svars['remaining_day'] = days_remaining
        svars['remaining_hour'] = hours_remaining
        svars['remaining_minute'] = minutes_remaining
        svars['remaining_second'] = seconds_remaining
        

##################################################################################################
# MEDIA FUNCTIONS
##################################################################################################


##################################################################################################
# GET FUNCTIONS
##################################################################################################


##################################################################################################
# PARSE FUNCTIONS
##################################################################################################
