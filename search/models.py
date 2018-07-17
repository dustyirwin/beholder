from django.db import models
from django.contrib.postgres.fields import JSONField

class SearchParams(models.Model):
    user = models.CharField(max_length=32)
    market_name = models.CharField(max_length=32)
    categories = JSONField(null=True, blank=True)
    search_filters = JSONField(null=True, blank=True)
