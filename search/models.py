from django.db import models
from django.contrib.postgres.fields import JSONField


class SessionData(models.Model):
    user = models.CharField(max_length=20)
    session_id = models.CharField(max_length=20)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.session_id+' '+self.user
