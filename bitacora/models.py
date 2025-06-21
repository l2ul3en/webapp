from django.db import models

class Electric(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    telephone = models.CharField(max_length=12, blank=False, null=False)

    def __str__(self) -> str:
        return self.name
    
class City(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self) -> str:
        return self.name            

class Cmts(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    ip = models.GenericIPAddressField(blank=False, null=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Node(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    ip = models.GenericIPAddressField(blank=True, null=True)
    mac = models.CharField(max_length=14, blank=True, null=True, help_text="Formato: AAAA-BBBB-CCCC")
    upstream = models.CharField(max_length=8, blank=True, null=True)
    downstream = models.CharField(max_length=8, blank=True, null=True)
    graph = models.URLField(blank=True, null=True)
    cmts = models.ForeignKey(Cmts, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    
class Source(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    ip = models.GenericIPAddressField(blank=True, null=True)
    mac = models.CharField(max_length=14, blank=True, null=True, help_text="Formato: AAAA-BBBB-CCCC")
    upstream = models.CharField(max_length=8, blank=True, null=True)
    downstream = models.CharField(max_length=8, blank=True, null=True)
    service_code = models.IntegerField(blank=False, null=False)
    graph = models.URLField(blank=True, null=True)
    cmts = models.ForeignKey(Cmts, on_delete=models.CASCADE)
    electric = models.ForeignKey(Electric, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name