from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Url(models.Model):
    url = models.URLField(blank=False)
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="urls")