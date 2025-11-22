from django.contrib import admin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from .models import Booking, EmailTemplate
from .utils import generate_booking_pdf, render_email_from_db


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "date", "time", "status", "created_at")
    list_filter = ("status", "date")
    search_fields = ("name", "email", "phone")
    ordering = ("-date", "-time")

    actions = ["confirm_bookings"]

    def confirm_bookings(self, request, queryset):
        """
        Admin action to confirm pending bookings, generate a PDF
        and email it to the customer.
        """
        count = 0

        for booking in queryset:
            if booking.status != Booking.Status.PENDING:
                continue  # only confirm pending ones

            booking.status = Booking.Status.CONFIRMED
            booking.save()

            # Generate PDF
            pdf_bytes = generate_booking_pdf(booking)

            # Email content from DB template (fallback to file)
            context = {"booking": booking}
            subject, body = render_email_from_db("booking_confirmed", context)
            if not subject:
                subject = "Your booking is confirmed"
                body = render_to_string("bookings/email_confirmed.txt", context)

            email = EmailMessage(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [booking.email],
            )

            # Attach PDF
            email.attach(
                f"booking_{booking.id}.pdf",
                pdf_bytes,
                "application/pdf",
            )

            email.send()
            count += 1

        self.message_user(request, f"{count} booking(s) confirmed.")

    confirm_bookings.short_description = "Confirm selected bookings"


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("key", "subject", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("key", "subject", "body")
    ordering = ("key",)
