from rest_framework import serializers
from rest_framework import generics
from .models import Enquiry
from .serializers import EnquirySerializer

class EnquiryListAPIView(generics.ListAPIView):
    queryset = Enquiry.objects.all().order_by('-created_at')
    serializer_class = EnquirySerializer;
