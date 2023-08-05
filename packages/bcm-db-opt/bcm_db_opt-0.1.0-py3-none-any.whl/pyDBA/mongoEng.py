from mongoengine import connect,  Document,EmbeddedDocument,EmbeddedDocumentField, StringField, IntField, DateField, DictField, ListField,ReferenceField,FloatField
import time
import datetime
connect('BCX', host='localhost', port=27017)
times = 100

class Nidus(Document):
    userID = StringField()
    studyID= StringField()
    seriesID= StringField()
    detectionRes= DictField()
    segmentRes = ListField(ListField(FloatField()))
    resgrssionRes= DictField()
    histogram= DictField()
    status= IntField()
    parent= StringField()
    nidusNo= IntField()
    sliceNo= IntField()
    distance = FloatField()
    categoryBI= DictField()
    categoryType= DictField()
    categoryMalignancy= DictField()
    categoryPosition= DictField()
    categoryShape= DictField()
    meta = {'collection':'nidus', 'strict': False}

class Series(Document):
    patientID = StringField()
    patientName= StringField()
    patientSex = StringField()
    patientBirth = DateField()
    date = DateField()
    description= StringField()
    studyID= StringField()
    seriesID= StringField()
    origin= StringField()
    nidus = ListField(ReferenceField(Nidus))
    meta = {'collection':'series', 'strict': False}
    

start = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d")
end = datetime.datetime.strptime("2020-12-31", "%Y-%m-%d")



startTime = time.time()
for  i in range(0, times):
    for series in Series.objects(patientBirth__gte=start, patientBirth__lt=end).skip(200 * 20).limit(20):
        for nidus in Nidus.objects(seriesID=series.seriesID):
            series.nidus.append(nidus)
        # print(series)

endTime = time.time()


print('共计耗时 ', (endTime - startTime )* 1000, 'ms')
print('平均耗时 ', (endTime - startTime) / times * 1000, 'ms')