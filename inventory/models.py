from django.db import models
from django.contrib.postgres.fields import JSONField


class ItemData(models.Model):
    name = models.CharField(max_length=256)
    item_id = models.CharField(max_length=32)
    data = JSONField(default={})

    def __str__(self):
        return self.item_id+' '+self.data['market']+' '+self.name[:75]
