from bson.objectid import ObjectId
from DBAccess import DBAccess 

from dataclasses import dataclass
from utils import format_filter

@dataclass
class Field:
    column_type: str
 
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        # print('Found model: %s' % name)
        # print('Found cls: %s' % cls)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                # print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings # mapping attr to field of collection
        new_cls = type.__new__(cls, name, bases, attrs)
        new_cls.collection = DBAccess.db[name] # collection name is the same as class name 
        return new_cls

class Model(object, metaclass=ModelMetaclass):
    def __init__(self, record={}) -> None:
        self.record = record
        super().__init__()
    def __getattr__(self, key):
        if self.record and len(self.record)>0:
            return self.record.get(key, None)
        else:
            return None
    def __setattr__(self, name: str, value) -> None:
        if name in type(self).__mappings__.keys():
            self.record[name] = value
        else:
            super().__setattr__(name, value)
    
    
    @classmethod
    @format_filter
    def find(cls, filter={}, currentPage=1, pageSize=10) -> list:
        if pageSize < 1:
            records = cls.collection.find(filter)
        else:
            records = cls.collection.find(filter).skip(pageSize*(currentPage-1)).limit(pageSize)
        return [cls(record) for record in records]
    
    @classmethod
    @format_filter
    def aggregate(cls, pipeline={}):
        records = cls.collection.aggregate(pipeline)
        return records

    @classmethod
    @format_filter
    def find_one(cls, filter=None):
        record = cls.collection.find_one(filter)
        return cls(record)

    @classmethod
    def insert_one(cls, record):
        return cls.collection.insert_one(record).inserted_id

    @classmethod
    def insert_many(cls, records):
        return cls.collection.insert(records)

    @classmethod
    @format_filter
    def update_one(cls, filter, record):
        return cls.collection.update_one(filter,  {'$set': record}).modified_count

    @classmethod
    @format_filter
    def update_many(cls, filter, record):
        return cls.collection.update_many(filter, {'$set': record}).modified_count

    @classmethod
    @format_filter
    def delete_one(cls, filter=None):
        result = cls.collection.delete_one(filter).deleted_count
        return result
    
    @classmethod
    @format_filter
    def delete_many(cls, filter=None):
        result = cls.collection.delete_many(filter).deleted_count
        return result


    @classmethod
    @format_filter
    def find_one_and_delete(cls, filter=None):
        record = cls.collection.find_one_and_delete(filter)
        return cls(record)
    
    @classmethod
    def count(cls):
        return cls.collection.count()
    
    @classmethod
    @format_filter
    def count_by(cls, filter):
        return cls.collection.find(filter).count()
    
    def save(self):
        if len(self.record) > 0:
            return self.collection.insert_one(self.record).inserted_id
        else:
            return ''
    
    def update(self, record):
        if not self.record:
            return self.collection.update_one(self.record,  {'$set': record}).modified_count
        else:
            return 0
    
    def __repr__(self) -> str:
        if not self.record or len(self.record) < 1:
            return f"{self.__class__.__name__}()"
        repr_str = f"{self.__class__.__name__}("
        for k, v in self.record.items():
            repr_str += f"{k}:{v}, "
        repr_str += ")"
        return repr_str
    pass