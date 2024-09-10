from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('pressing_manager', 'Pressing Manager'),
        ('deliver', 'Deliver'),
        ('client', 'Client'),
    )
    
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='client')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


class Contact(models.Model):
    email = models.EmailField()
    description = models.TextField()
    service_rate = models.CharField(max_length=50)  # Numeric rating or choice-based field
    date = models.DateField(auto_now_add=True)  # Automatically set the date to now
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.email



class PressingProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255, default='Center')  # Default value for region
    city = models.CharField(max_length=255, default='Yaoundé')   # Default value for city
    quarter = models.CharField(max_length=255, default='Mendong') # Default value for quarter  # New field for quarter
    telephone_number = models.CharField(max_length=20, blank=True, null=True)  # New field for telephone
    email = models.EmailField(blank=True, null=True)  # New field for email
    services_offered = models.TextField()
    pricing = models.TextField()
    photos = models.ManyToManyField('Photo', blank=True)
    videos = models.ManyToManyField('Video', blank=True)
    about_us = models.TextField()
    approved = models.BooleanField(default=False)
    pressing_count = models.IntegerField(default=1)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    tiktok_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.business_name

class Photo(models.Model):
    image = models.ImageField(upload_to='pressing_photos/')
    
    def __str__(self):
        return f"Photo {self.id}"

class Video(models.Model):
    video_file = models.FileField(upload_to='pressing_videos/')
    
    def __str__(self):
        return f"Video {self.id}"


class Receipt(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pdf = models.FileField(upload_to='receipts/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Receipt {self.id}'


class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.message[:20]}"



