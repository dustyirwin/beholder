from django.db import models
from django.contrib.postgres.fields import JSONField


class ItemData(models.Model):
    name = models.CharField(max_length=256)
    item_id = models.CharField(max_length=32)
    data = JSONField(default=dict)

    def __str__(self):
        return f"{self.item_id} {self.data['market_name']} {self.name[:75]}"
