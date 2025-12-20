from django.db import models


class Example(models.Model):
    text = models.CharField(max_length=10)

    class Meta:
        ordering = ("id",)
