from django.db import models

class Enquiry(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fullname} - {self.subject}"

class Booking(models.Model):
    trip_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    arrival_date = models.DateField()
    adults = models.IntegerField()
    children = models.IntegerField()
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.trip_name}"