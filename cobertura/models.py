from django.db import models

class Node(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    coverage = models.CharField(max_length=250, blank=False, null=False)
    subscriber = models.IntegerField(blank=False,null=False)

    def __str__(self) -> str:
      return self.name

