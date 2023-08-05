from Model import Model, Field
from Role import Role
from bson.objectid import ObjectId


class User(Model):
    userName = Field("str")
    realName = Field("str")
    roles = Field("[str]")
    password = Field("str")
    
    @classmethod
    def find_withRole(cls, filter={}, currentPage=1, pageSize=10) -> list:
        records = cls.find(filter=filter, currentPage=currentPage, pageSize=pageSize)
        for record in records:
            record.record['roles'] = Role.find({'_id':{'$in':[ObjectId(_id) for _id in record.roles]}}, pageSize=-1)
        return records

    @classmethod
    def find_one_withRole(cls, filter={}):
        record = cls.find_one(filter)
        if record.record is not None:
            record.record['roles'] = Role.find({'_id':{'$in':[ObjectId(_id) for _id in record.roles]}}, pageSize=-1)
        return record
