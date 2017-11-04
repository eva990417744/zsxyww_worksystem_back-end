from django.test import TestCase
from datetime import datetime,timedelta

e = datetime.strptime('2017-4-22', '%Y-%m-%d')
s = datetime.strptime('2017-4-22', '%Y-%m-%d')
if e-s<=timedelta(days=1):
    print(s-timedelta(minutes=1))
else:
    print(2)