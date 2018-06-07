from django.db import models
from django.contrib.postgres.fields import JSONField
# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    phone = models.CharField(max_length=11)
    data = JSONField(default={})

    def __str__(self):
        return self.item_id+' '+self.name
