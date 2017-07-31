import exrates as ex
import datetime
import time
import os
import subprocess



tests = []
def addTestNum(num, passed):
    if(not passed):
        tests.append(num)

# Test exrates.py:
# Fetching from url:
# 1.1

print("fetching test:")
addTestNum(1.1, ex._fetch_currencies() != -1)
if(1.1 in tests):
    exit(1)
    
# Fetching from url:
# 2.1
print("fetching with datetime.date test:")
addTestNum(2.1, ex._fetch_exrates(datetime.date(2007, 5, 3)) != -1)
if(2.1 in tests):
    exit(1)
# 2.2
print("empty string test:")
addTestNum(2.2, ex._fetch_exrates('') != -1)
# 2.3
print("valid string test:")
addTestNum(2.3, ex._fetch_exrates('2007-05-03') != -1)
# 2.4
print("character in date test:")
addTestNum(2.4, ex._fetch_exrates('20a7-05-03') == -1)
# 2.5
print("invalid month test:")
addTestNum(2.5, ex._fetch_exrates('2007-33-03') == -1)
# 2.6
print("invalid day test:")
addTestNum(2.6, ex._fetch_exrates('2007-05-32') == -1)
# 2.7
print("wrong format test:")
addTestNum(2.7, ex._fetch_exrates('20070413') == -1)

# 3.1
print("_save_currencies no dictionary")
addTestNum(3.1, ex._save_currencies(1) == -1)
# 3.2
print("_save_currencies no dictionary")
addTestNum(3.2, ex._save_currencies('eqw') == -1)
# 3.3
print("_save_currencies no dictionary")
addTestNum(3.3, ex._save_currencies([1, 3]) == -1)

# 4.1
print("get currencies test:")
addTestNum(4.1, ex._get_currencies() != -1)

# 5.1
print("get exrates test:")
addTestNum(5.1, ex._get_exrates('') != -1)

# 5.2
addTestNum(5.2, ex._get_exrates("1939-05-03") == -1)
# 5.3
addTestNum(5.3, ex._get_exrates('20a7-05-03') == -1)


if (len(tests) != 0):
    print('{} false tests:'.format(len(tests)))
    for test in tests:
        print(test)
else:
    print("test completed with no errors")
