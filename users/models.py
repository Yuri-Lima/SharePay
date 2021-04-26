from typing import AbstractSet
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, null= True, blank= True)
    last_name = models.CharField(max_length=100, null= True, blank= True)
    def __str__(self):
        if self.first_name and self.last_name:
            fullname = self.first_name + ' ' + self.last_name
            return fullname
        else:
            return self.username

