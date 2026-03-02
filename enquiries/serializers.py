from rest_framework import serializers
from .models import Enquiry, Booking

class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = '__all__'
        read_only_fields = ["id", "created_at"]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"