from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('deliver', 'Deliver'),
        ('client', 'Client'),
    )
    
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='client')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)




class Contact(models.Model):
    email = models.EmailField()
    description = models.TextField()
    service_rate = models.CharField(max_length=50)  # You can also use IntegerField with choices if it's a numeric rating
    date = models.DateField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.email
    