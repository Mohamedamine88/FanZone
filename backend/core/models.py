from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MatchType(models.TextChoices):
    CAN = 'CAN', _('CAN 2025')
    WORLD_CUP = 'WORLD_CUP', _('World Cup 2030')
    GROUP_STAGE = 'GROUP_STAGE', _('Group Stage')
    ROUND_OF_16 = 'ROUND_OF_16', _('Round of 16')
    QUARTER_FINALS = 'QUARTER_FINALS', _('Quarter Finals')
    SEMI_FINALS = 'SEMI_FINALS', _('Semi Finals')
    FINAL = 'FINAL', _('Final')

class ActivityType(models.TextChoices):
    MUSEUM = 'MUSEUM', _('Museum')
    TRAVEL = 'TRAVEL', _('Travel')
    SPORT = 'SPORT', _('Sport')
    ENTERTAINMENT = 'ENTERTAINMENT', _('Entertainment')
    CULTURE = 'CULTURE', _('Culture')
    SHOPPING = 'SHOPPING', _('Shopping')
    FOOD = 'FOOD', _('Food & Dining')
    NIGHTLIFE = 'NIGHTLIFE', _('Nightlife')
    TOUR = 'TOUR', _('Tour')
    WORKSHOP = 'WORKSHOP', _('Workshop')
    EXHIBITION = 'EXHIBITION', _('Exhibition')
    CONCERT = 'CONCERT', _('Concert')
    FAN_ZONE = 'FAN_ZONE', _('Fan Zone')

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airline = models.CharField(max_length=100, null=True, blank=True)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.airline or 'Unknown'} - {self.flight_number}"

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available_rooms = models.IntegerField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

class MatchTicket(models.Model):
    match_name = models.CharField(max_length=200)
    match_date = models.DateTimeField()
    stadium = models.CharField(max_length=200)
    match_type = models.CharField(max_length=20, choices=MatchType.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_tickets = models.IntegerField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.match_name

class Activity(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    city = models.CharField(max_length=100)
    activity_date = models.DateTimeField()
    activity_type = models.CharField(max_length=20, choices=ActivityType.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_spots = models.IntegerField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} in {self.city}"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ManyToManyField(Flight, blank=True)
    hotel = models.ManyToManyField(Hotel, blank=True)
    match_ticket = models.ManyToManyField(MatchTicket, blank=True)
    activity = models.ManyToManyField(Activity, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user.username}"

class Package(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    flights = models.ManyToManyField(Flight)
    hotels = models.ManyToManyField(Hotel)
    match_tickets = models.ManyToManyField(MatchTicket)
    activities = models.ManyToManyField(Activity)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
