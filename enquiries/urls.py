from django.urls import path
from .views import (
    EnquiryListCreateAPIView,
    EnquiryDestroyAPIView,
    BookingCreateAPIView,
    BookingDestroyAPIView,
    ReviewListCreateAPIView,
    ReviewAdminListAPIView,
    ReviewApproveAPIView,
    ReviewDestroyAPIView,
)

urlpatterns = [
    path("enquiries/", EnquiryListCreateAPIView.as_view(), name="enquiry-list-create"),
    path("enquiries/<int:pk>/", EnquiryDestroyAPIView.as_view(), name="enquiry-delete"),
    path("bookings/", BookingCreateAPIView.as_view(), name="booking-create"),
    path("bookings/<int:pk>/", BookingDestroyAPIView.as_view(), name="booking-delete"),
    path("reviews/", ReviewListCreateAPIView.as_view(), name="review-list-create"),
    path("reviews/all/", ReviewAdminListAPIView.as_view(), name="review-admin-list"),
    path("reviews/<int:pk>/approve/", ReviewApproveAPIView.as_view(), name="review-approve"),
    path("reviews/<int:pk>/", ReviewDestroyAPIView.as_view(), name="review-delete"),
]