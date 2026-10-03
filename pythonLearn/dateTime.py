import datetime

today = datetime.date.today()
print(today)
now = datetime.datetime.now()
print(now)

target_datetime = datetime.datetime(2002, 9,9, 5, 30, 50)
current_datetime = datetime.datetime.now()

if target_datetime < current_datetime:
    print("Target date time has passed")
else:
    print("Target date time has NOT passed")