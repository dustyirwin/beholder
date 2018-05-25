from django.db import models
from django.utils.timezone import now
from django.contrib.postgres.fields import JSONField


class Amazon(models.Model):
    name = models.CharField(max_length=200)
    ASIN = models.CharField(max_length=10)
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
    alibabaId = models.CharField(max_length=14)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.itemId+' '+self.name


class Walmart(models.Model):
    name = models.CharField(max_length=200)
    itemId = models.CharField(max_length=14)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.itemId+' '+self.name

class Target(models.Model):
    name = models.CharField(max_length=200)
    itemId = models.CharField(max_length=14)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.itemId+' '+self.name
