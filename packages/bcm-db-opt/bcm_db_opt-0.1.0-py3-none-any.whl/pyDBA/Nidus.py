from Model import Model, Field
from bson.objectid import ObjectId


class Nidus(Model):
    userID = Field("str")
    studyID = Field("str")
    seriesID = Field("str")
    detectionRes = Field("dict")
    segmentRes = Field("[[float]]")
    resgrssionRes =  Field("dict")
    histogram =  Field("dict")
    status =  Field("int")
    parent =  Field("str")
    nidusNo =  Field("int")
    sliceNo = Field("int")
    distance = Field("float")
    categoryBI = Field("dict")
    categoryType =  Field("dict")
    categoryMalignancy = Field("dict")
    categoryPosition = Field("dict")
    categoryShape =  Field("dict")