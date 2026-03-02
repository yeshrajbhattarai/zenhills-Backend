from django.contrib import admin
from .models import Enquiry, Booking


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "phone", "subject", "created_at")
    search_fields = ("fullname", "email", "phone", "subject")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "trip_name",
        "full_name",
        "email",
        "phone",
        "arrival_date",
        "adults",
        "children",
        "created_at",
    )
    search_fields = ("trip_name", "full_name", "email", "phone")
    list_filter = ("arrival_date", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)