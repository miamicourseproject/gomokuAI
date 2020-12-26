from datetime import datetime
now = datetime.now()
a = now.strftime("%H:%M:%S")
b = datetime.strptime("10:33:26", "%H:%M:%S")
print(now-b)

# from datetime import datetime
# s1 = '10:33:26'
# s2 = '11:15:49' # for example
# FMT = '%H:%M:%S'
# tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
# print(tdelta)