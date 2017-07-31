"""
Name: Dor Wiser

module exrates that implements fetching, saving, and analysis of the historical exchange rates
"""

import csv
import datetime
import json
import os
from urllib.error import URLError, HTTPError
import urllib.request


userID = "b0a1d1e058124432a991b891eaab2710"  # My UserID For openexchangerates.org. if it's not working please change it to valid one
someError = -1  # Default Case: Will return an empty dictionary

# If there is no data folder create one
if(os.path.exists("data") == False):
    os.makedirs("data")
    
# that fetches the currencies list from here (http://openexchangerates.org/api/currencies.json) 
#and returns it as a dictionary

def _fetch_currencies():
    # fetch from URL:
    
    try:
        url = urllib.request.urlopen("http://openexchangerates.org/api/currencies.json")
    except HTTPError as e:
        print('Error code: ', e.code)
        return someError
    except URLError as e:
        print('Reason: ', e.reason)
        return someError
    else:
        urlData = json.loads(url.read().decode())
        # print("Fetched Successfully")
        if(len(urlData) == 0):
            print("No Data for specific date")
            return someError
        
    return urlData

#fetches the exchange rates for the date date from the Open Exchange Rates (https://openexchangerates.org/) 
#website and returns it as a dictionary.

def _fetch_exrates(date):
    
    # Date Type Check:
    
    if(checkDate(date) == False):
        return someError
    
    # String to Date conversion:
    date = strToDate(date)
    # fetch from URL:
    
    try: 
        url = urllib.request.urlopen("https://openexchangerates.org/api/historical/{}.json?app_id={}".format(date.__str__(), userID))
    except HTTPError as e:
        print('Error code: ', e.code)
        return someError
    except URLError as e:
        print('Reason: ', e.reason)
        return someError
    else:
        urlData = json.loads(url.read().decode())['rates']
        if(len(urlData) == 0):
            print("No Data for specific date")
            return someError
        # print("Fetched Successfully")
    return urlData

def _save_currencies(currencies):
    if(isinstance(currencies, dict) == False):
        print("invalid currencies type - Should be a Dictionary")
        return someError
    joinDict = currencies

    fpath = os.path.join("data", 'currencies.csv')
    if(os.path.isfile(fpath)):
        dict1 = _load_currencies()
        joinDict.clear()
        joinDict = {**currencies, **dict1}
    try:
        with open(fpath, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Code', 'Name'])
            for key, value in joinDict.items():
                writer.writerow([key, value])  
            # print("saved successfully")
    except (OSError, IOError) as e:
        print('Error code: ', e.code)
        exit(1)
    
#Function returns the currencies loaded from the currencies file

def _load_currencies():

    fpath = os.path.join("data", 'currencies.csv')
    try:
        with open(fpath, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            return dict(reader)
    except (OSError, IOError) as e:
        print('Error code: ', e.code)
        exit(1)

#returns the currencies loaded from the currencies file, as a dictionary.
#If the currencies file doesn't exists, the function fetches the data from the internet,
#saves it to the currencies file and then returns it.

def _get_currencies():
    fpath = os.path.join("data", 'currencies.csv')
    if(os.path.isfile(fpath) == False):
        dict1 = _fetch_currencies()
        _save_currencies(dict1)
    return _load_currencies()
    
#saves the exchange rates data for date date in the appropriate exchange rates file

def _save_exrates(date, rates):
    if(checkDate(date) == False):
        return someError
    if(isinstance(rates, dict) == False):
        print("invalid rates type - Should be a Dictionary")
        return someError
    # String to Date conversion:
    date = strToDate(date)
    joinDict = rates
    fpath = os.path.join("data", '{}.csv'.format(str(date)))
    if(os.path.isfile(fpath)):
        dict1 = _load_exrates()
        joinDict.clear()
        joinDict = {**rates, **dict1}
    try:
        with open(fpath, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Code', 'Rate'])
            for key, value in joinDict.items():
                writer.writerow([key, value])  
            # print("saved successfully")
    except (OSError, IOError) as e:
        print('Error code: ', e.code)
        return someError

#that returns the exchange rates data for date date loaded from the appropriate exchange rates file.

def _load_exrates(date):
    if(checkDate(date) == False):
        return someError
    date = strToDate(date)
    fpath = os.path.join("data", '{}.csv'.format(str(date)))
    try:
        with open(fpath, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            return dict(reader)
    except (OSError, IOError) as e:
        print('Error code: ', e.code)
        return someError

#that returns the exchange rates data for date date loaded from the appropriate exchange rates file. 
#If that file doesn't exists, the function fetches the data from the internet, saves it to the file, and then returns it.

def _get_exrates(date):
    if(checkDate(date) == False):
        return someError
    # String to Date conversion:
    date = strToDate(date)
    fpath = os.path.join("data", '{}.csv'.format(str(date)))
    if(not os.path.isfile(fpath)):
        dict1 = _fetch_exrates(date)
        if(dict1 == -1):
            return someError
        _save_exrates(date, dict1)
    return _load_exrates(date)
    
#gets variable and checking if it's a valid date type

def checkDate(date):
    if(isinstance(date, datetime.date) == False):
        if(isinstance(date, str)):
            if(date == ''):
                return True
            else:
                # Does date have 2 "-"
                dc = date.split("-")
                if(len(dc) != 3):
                    print('Wrong Date Format %Y-%m-%d')
                    return False
                # Does date in right length Or Not valid
                for d in dc:
                    if(d.isdigit() == False):
                        print('Invalid input')
                        return False
                # Year
                if(len(dc[0]) != 4):
                    print('Wrong Year Input')
                    return False
                # Month
                if(len(dc[1]) != 2):
                    print('Wrong Month Input')
                    return False
                if(int(dc[1]) < 1 or int(dc[1]) > 12):
                    print('Wrong Month Input')
                    return False
                # Day
                if(len(dc[2]) != 2):
                    print('Wrong Day Input')
                    return False
                if(int(dc[2]) < 1 or int(dc[2]) > 31):
                    print('Wrong Day Input')
                    return False
        else:
            print("Invalid Date Type. Please use date as DateTime.Date or String Object")
            return False
    return True

#deals with string type date and returns it as a datetime.date

def strToDate(date):
    # String to Date conversion:
    if(isinstance(date, str)):
        if(date == ''):
            date = datetime.date.today()
        else:
            datetime.datetime.strptime(date, "%Y-%m-%d").date()
    return date
