from django.db import models
from django.contrib.auth.models import User
class EncodedImage(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    part_a = models.TextField()
    part_b = models.TextField()