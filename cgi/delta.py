import  datetime
from datetime import date, datetime,timedelta

def datespan (startDate, endDate, delta=timedelta(days=1)):
	currentDate = startDate
	while currentDate < endDate:
		yield currentDate
		currentDate += delta

	for day in datespan(date(2007, 3, 30), date(2007, 4, 3),
				delta=timedelta(days=1)):
	print day
