from typing import AbstractSet
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, null= True, blank= True)
    last_name = models.CharField(max_length=100, null= True, blank= True)
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        if self.first_name and self.last_name:
            fullname = self.first_name + ' ' + self.last_name
            return fullname
        else:
            return self.username

    def clean(self):
        pass
        # self.first_name = self.first_name.capitalize()
        # self.last_name = self.last_name.capitalize()
        
    def get_absolute_url(self):
        return reverse("users:update", kwargs={"pk": self.pk})
    
