import os
import json
import logging
import requests
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Enquiry, Booking, Review
from .serializers import EnquirySerializer, BookingSerializer, ReviewSerializer

logger = logging.getLogger(__name__)

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")


def send_email(to_email: str, to_name: str, subject: str, body: str):
    if not RESEND_API_KEY:
        logger.error("RESEND_API_KEY is not set — email not sent.")
        return

    payload = {
        "from": "ZenHills Journeys <noreply@zenhillsjourneys.com>",
        "to": [f"{to_name} <{to_email}>"],
        "subject": subject,
        "text": body,
    }

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps(payload),
            timeout=10,
        )
        if response.status_code == 200:
            logger.info(f"Email sent to {to_email} ✅")
        else:
            logger.error(f"Resend error {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Resend request failed: {e}")


# ─── Enquiry ──────────────────────────────────────────────────────────────────
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

    def perform_create(self, serializer):
        enquiry = serializer.save()
        send_email(
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


class EnquiryDestroyAPIView(generics.DestroyAPIView):
    serializer_class = EnquirySerializer

    def get_queryset(self):
        return Enquiry.objects.all()

    def delete(self, request, *args, **kwargs):
        expected_key = os.environ.get("ADMIN_KEY", "")
        incoming_key = request.headers.get("X-Admin-Key", "")
        if not expected_key or incoming_key != expected_key:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)


# ─── Booking ──────────────────────────────────────────────────────────────────
class BookingCreateAPIView(generics.ListCreateAPIView):
    queryset = Booking.objects.all().order_by("-created_at")
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        expected_key = os.environ.get("ADMIN_KEY", "")
        incoming_key = request.headers.get("X-Admin-Key", "")
        if not expected_key or incoming_key != expected_key:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        booking = serializer.save()

        send_email(
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

        send_email(
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

📞 +91 9474090064 | +91 8409970064
💬 WhatsApp: https://wa.me/918409970064
🌐 https://zenhillsjourneys.com

Warm regards,
ZenHills Journeys Team
Gangtok, Sikkim
""",
        )


class BookingDestroyAPIView(generics.DestroyAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.all()

    def delete(self, request, *args, **kwargs):
        expected_key = os.environ.get("ADMIN_KEY", "")
        incoming_key = request.headers.get("X-Admin-Key", "")
        if not expected_key or incoming_key != expected_key:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)
    
    
# ─── Reviews ─────────────────────────────────────────────────────────────────
class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(is_approved=True).order_by("-created_at")

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ReviewAdminListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all().order_by("-created_at")

    def get(self, request, *args, **kwargs):
        expected_key = os.environ.get("ADMIN_KEY", "")
        incoming_key = request.headers.get("X-Admin-Key", "")
        if not expected_key or incoming_key != expected_key:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)


class ReviewApproveAPIView(APIView):
    def patch(self, request, pk):
        expected_key = os.environ.get("ADMIN_KEY", "")
        incoming_key = request.headers.get("X-Admin-Key", "")
        if not expected_key or incoming_key != expected_key:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get("action")
        if action == "approve":
            review.is_approved = True
        elif action == "reject":
            review.is_approved = False
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        review.save()
        return Response(ReviewSerializer(review).data)


class ReviewDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def delete(self, request, *args, **kwargs):
        expected_key = os.environ.get("ADMIN_KEY", "")
        incoming_key = request.headers.get("X-Admin-Key", "")
        if not expected_key or incoming_key != expected_key:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)