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






class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='towns')

    def __str__(self):
        return self.name


class Quarter(models.Model):
    name = models.CharField(max_length=255)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='quarters')

    def __str__(self):
        return self.name


class PressingProfile(models.Model):
    business_name = models.CharField(max_length=255)
    telephone_number = models.CharField(max_length=15, null=False, default=0000000)
    email = models.EmailField(null=True, blank=True)
    services_offered = models.TextField()
    pricing = models.TextField()
    about_us = models.TextField()
    pressing_count = models.IntegerField(default=0)  # Add this line
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    town = models.ForeignKey(Town, on_delete=models.SET_NULL, null=True)
    quarter = models.ForeignKey(Quarter, on_delete=models.SET_NULL, null=True)
    photos = models.ImageField(upload_to='photos/', blank=True, null=True)
    videos = models.FileField(upload_to='videos/', blank=True, null=True)
    tiktok_url = models.URLField(max_length=200, blank=True, null=True)
    instagram_url = models.URLField(max_length=200, blank=True, null=True)
    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    youtube_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.business_name


class PressingLocation(models.Model):
    pressing_profile = models.ForeignKey(PressingProfile, on_delete=models.CASCADE, related_name='locations')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pressing_profile.business_name} - {self.region.name}, {self.town.name}, {self.quarter.name}"


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    pressing_profile = models.ForeignKey(PressingProfile, related_name='photo_set', on_delete=models.CASCADE)


class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')
    pressing_profile = models.ForeignKey(PressingProfile, related_name='video_set', on_delete=models.CASCADE)








class Geolocation(models.Model):
    PICKUP = 'pickup'
    DELIVERY = 'delivery'

    LOCATION_TYPE_CHOICES = [
        (PICKUP, 'Pickup'),
        (DELIVERY, 'Deliver Dressing'),
    ]

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_type = models.CharField(
        max_length=10,
        choices=LOCATION_TYPE_CHOICES,
        default=DELIVERY,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_location_type_display()} - Lat: {self.latitude}, Long: {self.longitude}"


class Delivery(models.Model):
    client_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, related_name='deliveries')

    def __str__(self):
        return f"{self.client_name} - {self.status}"

class Invoice(models.Model):
    client_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Invoice {self.id} - {self.client_name}"

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


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



class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms')

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'