from tortoise import fields
from tortoise.models import Model

class User(Model):
    id=fields.IntField(primary_key=True)
    name= fields.CharField(max_length = 20)
    email= fields.CharField(max_length=35 , unique=True)
    password=fields.CharField(max_length=20)