from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Events(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=200)
    site = models.URLField()

    def __str__(self) -> str:
        return self.name