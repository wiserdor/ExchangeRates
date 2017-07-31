"""
Name: Dor Wiser

program get date input from user and prints the exchange rates for that date in a tabular form
"""

import exrates as ex
import sys
# There are some currencies that give an encoding error (ie. São Tomé and Príncipe Dobra), i used this function to prevent errors
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
currencies = ex._get_currencies()

print('Welcome to ERT ("Exchange Rates Table")')

while True:
    # Check currencies
    while True:
        if(currencies == -1):
            print("Error with getting the currencies. please check internet connection and try again")
            choice = input("Y - for trying again , anything else - for exit\n")
            if(choice == 'Y' or choice == 'y'):
                currencies = ex._get_currencies()
            else:
                print("Bye")
                exit(1)
        else:
            break
        
    # Get user date input
    while True:
        date = input('Please enter a date (YYYY-MM-DD):\n')
        rates = ex._get_exrates(date)
        if(rates == -1):
            input('Please enter a date (YYYY-MM-DD):\n')
        else:
            break
    multiDict = {}
    print("")
    for key in sorted(currencies.keys()):
        fl = rates.get(key, "")
        if(fl != ""):
            curFormat = '{:<30} {} {:>15.5f}'
        else:
            curFormat = '{:<30} {} {:>15}'
        uprint(curFormat.format("-" if fl == "" else currencies.get(key), '({})'.format(key), "-" if fl == "" else float(fl)))
    choice = input("Y - Continue , anything else - for exit\n")
    if(not (choice == 'Y' or choice == 'y')):
        print("Bye")
        exit(1)
        
