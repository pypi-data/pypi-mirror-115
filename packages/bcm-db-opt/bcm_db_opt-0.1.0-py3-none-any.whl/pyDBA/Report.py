from Model import Model, Field

class Report(Model):
    userID = Field("str")
    studyID = Field("str")
    reportFinding = Field("str")
    reportAdvice = Field("str")
    modifyTime = Field("Date")
    pass