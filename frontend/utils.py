import os
import re
from datetime import date
import numpy as np
import pandas as pd
import holidays

def get_all_file_paths(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

def extract_pred_dates_from_paths(paths):
    pattern = r'inference_\d+_(\d+)\.csv'
    pred_dates = []
    for path in paths:
        match = re.search(pattern, path)
        if match:
            pred_dates.append(match.group(1))
    return pred_dates

def get_holidays(country: str, year: int):
    """
    Retrieve all holidays for a given country and year.
    
    :param country: Country code (e.g., 'US' for United States).
    :param year: Year for which to retrieve holidays.
    :return: List of holiday dates.
    """
    # Define the country holidays instance
    country_holidays = holidays.CountryHoliday(country, years=year)
    
    # Get all holidays for the specified year
    holiday_dates = list(country_holidays.keys())
    
    return holiday_dates

def get_date_from_date_id(date_id, total_data_ids=480, holidays=[]):
    """
    Calculate the date from a given date_id, considering only business days.
    
    :param date_id: The ID to convert.
    :param total_data_ids: The total number of date IDs.
    :param holidays: A list of holiday dates to exclude.
    :return: The calculated business date.
    """
    # Convert today's date to the correct format explicitly
    today = np.datetime64(date.today(), 'D')  # Ensure it is 'D' type datetime64
    
    # Calculate the number of days to subtract
    days_to_subtract = total_data_ids - date_id
    
    # Ensure holidays are in the correct datetime64[D] format
    if holidays:
        holidays_np = np.array(holidays, dtype='datetime64[D]')
    else:
        holidays_np = np.array([], dtype='datetime64[D]')  # Ensure it's an empty datetime64 array if no holidays

    # Calculate business days, making sure all datatypes align for numpy operations
    business_days = np.busday_offset(today, -days_to_subtract, roll='forward', holidays=holidays_np)

    return business_days

# Function to convert the timestamp values to meaningful time format
def convert_to_meaningful_time(row_id, holidays=[]):
    # Extracting the date part from row_id and converting to integer
    date_id = int(row_id.split('_')[0])
    base_time = get_date_from_date_id(date_id, holidays=holidays)
    ts = int(row_id.split('_')[1])
    return base_time + pd.to_timedelta('15:51:00') + pd.Timedelta(seconds=ts)
