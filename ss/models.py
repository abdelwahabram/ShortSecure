from django.db import models

# Create your models here.

class Url(models.Model):
    url = models.URLField(blank=False)
