from Nidus import Nidus
from Model import Model, Field
from bson.objectid import ObjectId


class Series(Model):
    patientID = Field("str")
    patientName = Field("str")
    patientSex = Field("str")
    patientBirth = Field("Date") 
    date = Field("Date")  
    description = Field("str")
    studyID = Field("str")
    seriesID = Field("str")
    origin = Field("str")

    
    @classmethod
    def find_withNidus(cls, filter={}, currentPage=1, pageSize=10) -> list:
        pipeline = [
            {"$project":{"__v":0}},
            {'$match':filter},
            {'$limit': pageSize},
            {'$skip': pageSize * (currentPage - 1)},
            {'$lookup': 
                {
                    'from': 'Nidus',
                    'localField': 'seriesID' ,
                    'foreignField': 'seriesID',
                    'as':  'nidus'
                }
            }
        ]
        records = cls.aggregate(pipeline=pipeline)
        
        return [Series(record) for record in records]

    @classmethod
    def find_one_withNidus(cls, filter={}):
        pipeline = [
            {"$project":{"__v":0}},
            {'$match':filter},
            {'$limit': 1},
            {'$lookup': 
                {
                    'from': 'Nidus',
                    'localField': 'seriesID' ,
                    'foreignField': 'seriesID',
                    'as':  'nidus'
                }
            }
        ]
        records = cls.aggregate(pipeline=pipeline)

        return [Series(record) for record in records]
