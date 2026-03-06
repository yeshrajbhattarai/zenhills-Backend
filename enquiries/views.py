# enquiries/views.py

import os
import logging
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Enquiry, Booking
from .serializers import EnquirySerializer, BookingSerializer
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


class EnquiryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EnquirySerializer

    def get_queryset(self):
        return Enquiry.objects.all().order_by("-created_at")

    def get(self, request, *args, **kwargs):
        expected_key = os.environ.get("ADMIN_KEY", "")
        incoming_key = request.headers.get("X-Admin-Key", "")
        if not expected_key or incoming_key != expected_key:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        enquiry = serializer.save()

        try:
            # ── 1. Internal notification to ZenHills team ─────────────────────
            send_mail(
                subject=f"New Enquiry: {enquiry.subject}",
                message=f"""
New Enquiry Received
────────────────────
Name:    {enquiry.fullname}
Email:   {enquiry.email}
Phone:   {enquiry.phone or "Not provided"}
Subject: {enquiry.subject}
Message: {enquiry.message}
Received At: {enquiry.created_at.strftime("%d %b %Y, %I:%M %p IST")}
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["zenhills53@gmail.com"],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Enquiry internal email failed for {enquiry.fullname}: {e}")

        try:
            # ── 2. Thank you confirmation to the customer ─────────────────────
            send_mail(
                subject="Thank You for Reaching Out – ZenHills Journeys",
                message=f"""Dear {enquiry.fullname},

Thank you for getting in touch with ZenHills Journeys!

We have received your enquiry and our team will get back to you within 24 hours.

─────────────────────────────
Your Enquiry Details
─────────────────────────────
Subject: {enquiry.subject}
Message: {enquiry.message}
─────────────────────────────

In the meantime, feel free to explore our packages at:
https://zenhills-journeys.vercel.app/trips

Or reach us directly:
📞 +91 9474090064 | +91 8409970064
💬 WhatsApp: https://wa.me/918409970064

Warm regards,
ZenHills Journeys Team
Gangtok, Sikkim
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[enquiry.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Enquiry confirmation email failed for {enquiry.email}: {e}")


class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        booking = serializer.save()

        try:
            # ── 1. Internal notification to ZenHills team ─────────────────────
            send_mail(
                subject=f"New Booking: {booking.trip_name}",
                message=f"""
New Booking Received
────────────────────
Trip:             {booking.trip_name}
Name:             {booking.full_name}
Email:            {booking.email}
Phone:            {booking.phone}
Arrival Date:     {booking.arrival_date}
Adults:           {booking.adults}
Children:         {booking.children}
Special Requests: {booking.special_requests or "None"}
Submitted At:     {booking.created_at.strftime("%d %b %Y, %I:%M %p IST")}
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["zenhills53@gmail.com"],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Booking internal email failed for {booking.full_name}: {e}")

        try:
            # ── 2. Thank you confirmation to the customer ─────────────────────
            send_mail(
                subject="Booking Confirmed – ZenHills Journeys 🏔️",
                message=f"""Dear {booking.full_name},

Thank you for booking with ZenHills Journeys!

We have received your booking request and our team will contact you shortly to confirm availability and share further details.

─────────────────────────────
Your Booking Summary
─────────────────────────────
Trip:         {booking.trip_name}
Arrival Date: {booking.arrival_date}
Adults:       {booking.adults}
Children:     {booking.children}
Special Requests: {booking.special_requests or "None"}
─────────────────────────────

Get ready for an unforgettable journey through the mountains of Sikkim!

If you have any questions in the meantime, feel free to reach out:
📞 +91 9474090064 | +91 8409970064
💬 WhatsApp: https://wa.me/918409970064
🌐 https://zenhills-journeys.vercel.app

Warm regards,
ZenHills Journeys Team
Gangtok, Sikkim
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Booking confirmation email failed for {booking.email}: {e}")