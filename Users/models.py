from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile/', blank=True, null=True, default='default_image.png')

    class Meta:
        db_table = 'customuser'

    def __str__(self):
        return self.username


