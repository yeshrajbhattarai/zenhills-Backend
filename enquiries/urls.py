
from django.urls import path
from .views import EnquiryListCreateAPIView, BookingCreateAPIView

urlpatterns = [
    path("enquiries/", EnquiryListCreateAPIView.as_view(), name="enquiry-list-create"),
    path("bookings/", BookingCreateAPIView.as_view(), name="booking-create"),
]