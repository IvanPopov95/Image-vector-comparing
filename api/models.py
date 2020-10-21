from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

class Person(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    vector = ArrayField(models.FloatField(), size=3, default=[0.0,0.0,0.0])

    def __str__(self):
        return '{0} {1}'.format(self.name, self.surname)