import datetime

dateInput = input("Enter the date (mm/dd/yyyy): ")
dateSplit = dateInput.split("/")

jrf_month = int(dateSplit[0])
jrf_day = int(dateSplit[1])
jrf_year = int(dateSplit[2])

jrf_date = datetime.datetime(jrf_year, jrf_month, jrf_day)

print("{:%B %d, %Y}".format(jrf_date))