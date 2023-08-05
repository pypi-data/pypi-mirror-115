
from Model import DBAccess
DBAccess('BCX', host="192.168.10.245", port=27017)

from Nidus import Nidus
from Series import Series
from bson.objectid import ObjectId
from Role import Role
from User import User
import datetime
import time


# print(Role.__dict__, Role.find_one)
# roles = Role.find(pageSize=-1)
# role = Role.find_one()
# print(roles)

# role = Role({"roleName":"te", "privileges":[1,2]})
# print(role.save())
# print(Role.delete_one({"roleName":"te"}))
# print(role.save())
# print(Role.find_one_and_delete({"roleName":"te"}))
# print(role.roleName)
# u = User.find_one()
# # print(u, u.roles)
# print(User.find())
# u = User.find_one_withRole({'userName':'iofskr'})
# print('has this user:', u)
# u = User.find_one_withRole({'userName':'iodfskr'})
# print('userName not found', u)


# print('find by id')
# print(Role.find(filter={'_id':ObjectId("60f928c5cc59ea53ba9ca301")}))

# print('find by id list')
# print(Role.find(filter={'_id':{"in":[ObjectId("6102626f3efa126e13461272"), ObjectId("60f928c5cc59ea53ba9ca301")]}}))

# # print(Series.find_one())
# # print(Series.find_one_withNidus())

# print(Series.count())
# print(Series.find_one_withNidus())
print(Series.find_one_withNidus())
# print(Series.find({'date':{'between':[datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"), datetime.datetime.strptime("2020-01-02", "%Y-%m-%d")]}}))

# print('num series of male:', Series.count_by({'patientSex':1}))
# print('num series of female:', Series.count_by({'patientSex':0}))
# print('num series from 2000-01-01 to 2000-01-03', Series.count_by({'date':{'between':[datetime.datetime.strptime("2000-01-01", "%Y-%m-%d"), datetime.datetime.strptime("2020-01-02", "%Y-%m-%d")]}}))

# print('num of categoryMalignancy is positive', Nidus.count_by({'categoryMalignancy.category':1}))
# print('diameter from 6 to 8:', Nidus.count_by({'detectionRes.diameter':{"between":[6, 8]}}))
# print('num of categoryMalignancy is positive and diameter from 6 to 8:', Nidus.count_by({'categoryMalignancy.category':1, 'detectionRes.diameter':{"between":[6, 8]}}))
# # print(Nidus.find_one())

# print(Nidus.find_one({'seriesID':"820000200212087830", 'studyID':'410000201607067701'}))
# print(Nidus.count())
# print(Nidus.count_by({'categoryType.category':0}))
# print(Nidus.count_by({'categoryMalignancy.category':0}))
