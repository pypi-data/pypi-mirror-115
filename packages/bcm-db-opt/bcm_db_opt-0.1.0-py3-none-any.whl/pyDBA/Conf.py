from Model import Model, Field

class Conf(Model):
    target = Field("str")
    name = Field("str")
    type = Field("str")
    value = Field("str")
    pass