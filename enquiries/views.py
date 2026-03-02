# enquiries/views.py

from rest_framework import generics
from .models import Enquiry, Booking
from .serializers import EnquirySerializer, BookingSerializer
from django.core.mail import send_mail
from django.conf import settings

class EnquiryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Enquiry.objects.all().order_by('-created_at')
    serializer_class = EnquirySerializer

class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()

        subject = f"New Booking: {booking.trip_name}"

        message = f"""
New Booking Received

Trip: {booking.trip_name}
Name: {booking.full_name}
Email: {booking.email}
Phone: {booking.phone}
Arrival Date: {booking.arrival_date}
Adults: {booking.adults}
Children: {booking.children}
Special Requests: {booking.special_requests}
Created At: {booking.created_at}
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ["zenhills53@gmail.com"],  # where you want to receive booking emails
            fail_silently=False,
        )