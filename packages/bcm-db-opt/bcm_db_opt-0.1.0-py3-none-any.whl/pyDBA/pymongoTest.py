from pymongo import MongoClient
import time
import datetime
database = 'series'
times = 100
client = MongoClient('192.168.10.245')
db = client.BCX
collection1 = db[database]
collection2= db['nidus']


idList = []
startTime = time.time()
for i in range(0, times):
    results = collection1.find({"patientBirth": {'$gte': datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"), '$lte': datetime.datetime.strptime("2020-01-01", "%Y-%m-%d") + datetime.timedelta(days=1)}}).limit(20).skip(20*200)
    for result in results:
        # nidus =  collection2.find({'seriesID': result['seriesID']})
        # for n in nidus:
        idList.append(result)
endTime = time.time()


print('共计耗时 ', (endTime - startTime )* 1000, 'ms')
print('平均耗时 ', (endTime - startTime) / times * 1000, 'ms')