# ExchangeRates - Made with python 3.5
####was made for learning purposes####
python module that by given date returns exchange rates of that date.
the module creates "/Data" folder if not exists which is used as a cache directory.

on a request ,the module check first if the given date is in "/Data" directory.
if not it will fetch the information from http://openexchangerates.org/api
and will save it as a cache.

to start:
	python cod.py 
or	python ert.py

Tests: 
	Test.py is testing the module exrates
	you can compile it with python Test.py
