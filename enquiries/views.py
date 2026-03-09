# enquiries/views.py

import os
import json
import logging
import requests
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Enquiry, Booking
from .serializers import EnquirySerializer, BookingSerializer
from django.conf import settings

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# !! FOR LOCAL TESTING: API key is set directly here
# !! FOR PRODUCTION: move this to WSGI env var and use os.environ.get() only
# ─────────────────────────────────────────────────────────────────────────────
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")


def send_sg_email(to_email: str, to_name: str, subject: str, body: str):
    """
    Sends plain-text email via SendGrid HTTP API.
    Works on PythonAnywhere free — no SMTP ports needed.
    """
    if not SENDGRID_API_KEY:
        logger.error("SENDGRID_API_KEY is not set — email not sent.")
        return

    payload = {
        "personalizations": [
            {
                "to": [{"email": to_email, "name": to_name}],
                "subject": subject,
            }
        ],
        "from": {
            "email": "noreply@zenhillsjourneys.com",   # ✅ Updated — domain authenticated
            "name":  "ZenHills Journeys",
        },
        "content": [
            {"type": "text/plain", "value": body}
        ],
    }

    try:
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps(payload),
            timeout=10,
        )
        if response.status_code == 202:
            logger.info(f"Email sent to {to_email} ✅")
        else:
            logger.error(f"SendGrid error {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"SendGrid request failed: {e}")


# ─── Enquiry ─────────────────────────────────────────────────────────────────
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

        # ── Internal notification to ZenHills team only
        send_sg_email(
            to_email="zenhills53@gmail.com",
            to_name="ZenHills Team",
            subject=f"New Enquiry: {enquiry.subject}",
            body=f"""New Enquiry Received
────────────────────
Name:    {enquiry.fullname}
Email:   {enquiry.email}
Phone:   {enquiry.phone or "Not provided"}
Subject: {enquiry.subject}
Message: {enquiry.message}
Received At: {enquiry.created_at.strftime("%d %b %Y, %I:%M %p IST")}
""",
        )


# ─── Booking ─────────────────────────────────────────────────────────────────
class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        booking = serializer.save()

        # ── 1. Internal notification to ZenHills team ────────────────────────
        send_sg_email(
            to_email="zenhills53@gmail.com",
            to_name="ZenHills Team",
            subject=f"New Booking: {booking.trip_name}",
            body=f"""New Booking Received
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
        )

        # ── 2. Confirmation email to customer ────────────────────────────────
        send_sg_email(
            to_email=booking.email,
            to_name=booking.full_name,
            subject="Booking Confirmed – ZenHills Journeys 🏔️",
            body=f"""Dear {booking.full_name},

Thank you for booking with ZenHills Journeys!

We have received your booking request and our team will contact you shortly to confirm availability and share further details.

─────────────────────────────
Your Booking Summary
─────────────────────────────
Trip:             {booking.trip_name}
Arrival Date:     {booking.arrival_date}
Adults:           {booking.adults}
Children:         {booking.children}
Special Requests: {booking.special_requests or "None"}
─────────────────────────────

Get ready for an unforgettable journey through the mountains of Sikkim!

If you have any questions, feel free to reach out:
📞 +91 9474090064 | +91 8409970064

💬 WhatsApp: https://wa.me/918409970064

🌐 https://zenhillsjourneys.com

Warm regards,
ZenHills Journeys Team
Gangtok, Sikkim
""",
        )