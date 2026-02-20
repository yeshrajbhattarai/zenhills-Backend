from django.urls import path
from .views import EnquiryListAPIView
urlpatterns = [
     path('enquiries/', EnquiryListAPIView.as_view()),
]
