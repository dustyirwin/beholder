from django.db import models
from django.contrib.postgres.fields import JSONField


class ItemData(models.Model):
    name = models.CharField(max_length=200)
    item_id = models.CharField(max_length=10)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.item_id+' '+self.name
