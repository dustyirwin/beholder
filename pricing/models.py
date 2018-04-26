from django.db import models
from django.contrib.postgres.fields import JSONField


class Amazon(models.Model):
    name = models.CharField(max_length=200, null=False)
    ASIN = models.CharField(max_length=10, null=False)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.ASIN+' '+self.name


class Ebay(models.Model):
    name = models.CharField(max_length=200)
    itemId = models.CharField(max_length=14)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.itemId+' '+self.name


class Alibaba(models.Model):
    name = models.CharField(max_length=200)
    aliId = models.CharField(max_length=14)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.itemId+' '+self.name


class Walmart(models.Model):
    name = models.CharField(max_length=200)
    walId = models.CharField(max_length=14)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.itemId+' '+self.name
