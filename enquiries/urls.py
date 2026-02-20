
from django.urls import path
from .views import EnquiryListCreateAPIView

urlpatterns = [
    path("enquiries/", EnquiryListCreateAPIView.as_view(), name="enquiry-list-create"),
]