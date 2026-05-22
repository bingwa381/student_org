from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ])
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    year_of_study = models.CharField(max_length=10, choices=[
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
        ('Graduate', 'Graduate'),
    ])
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    payment_amount = models.PositiveIntegerField(default=10000)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    payment_confirmed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.registration_number or 'Pending'}"
