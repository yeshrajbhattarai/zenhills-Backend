# enquiries/views.py

from rest_framework import generics
from .models import Enquiry
from .serializers import EnquirySerializer


class EnquiryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Enquiry.objects.all().order_by('-created_at')
    serializer_class = EnquirySerializer