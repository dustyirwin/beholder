from django.db import models
from django.contrib.postgres.fields import JSONField


class SessionData(models.Model):
    user = models.CharField(max_length=32)
    session_id = models.CharField(max_length=32)
    data = JSONField(default={})

    def __str__(self):
        return self.session_id+' '+self.user
