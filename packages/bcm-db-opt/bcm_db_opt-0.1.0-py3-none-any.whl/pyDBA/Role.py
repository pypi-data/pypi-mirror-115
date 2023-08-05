from Model import Model, Field

class Role(Model):
    roleName = Field("str")
    privileges = Field("[int]")
    pass