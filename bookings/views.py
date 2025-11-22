from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import json  # <-- NEW

from .forms import BookingForm
from .utils import render_email_from_db
from .models import Booking


def booking_create(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()  # status = PENDING by default

            # context for templates
            context = {"booking": booking}

            # 1) Email to customer – booking received
            subject_user, body_user = render_email_from_db("booking_received", context)
            if not subject_user:
                # Fallback if no template defined in DB
                subject_user = "Your booking is being processed"
                body_user = (
                    f"Dear {booking.name},\n\n"
                    f"Thank you for your booking on {booking.date} at {booking.time}.\n"
                    "Your request has been received and is being processed.\n"
                    "You will receive a confirmation email once it is approved.\n\n"
                    "Best regards,\n"
                    "[APP_NAME]"
                )

            send_mail(
                subject_user,
                body_user,
                settings.DEFAULT_FROM_EMAIL,
                [booking.email],
            )

            # 2) Email to admin – new booking notification
            subject_admin, body_admin = render_email_from_db("new_booking_admin", context)
            if not subject_admin:
                subject_admin = "New booking submitted"
                body_admin = (
                    f"New booking received:\n\n"
                    f"Name: {booking.name}\n"
                    f"Email: {booking.email}\n"
                    f"Phone: {booking.phone}\n"
                    f"Date/Time: {booking.date} {booking.time}\n"
                    f"Status: {booking.status}\n"
                )

            send_mail(
                subject_admin,
                body_admin,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
            )

            messages.success(
                request,
                "Your booking has been submitted. Please check your email."
            )
            return redirect("booking_success")
    else:
        form = BookingForm()

    return render(request, "bookings/booking_form.html", {"form": form})


def booking_success(request):
    return render(request, "bookings/booking_success.html")


@staff_member_required
def admin_dashboard(request):
    """Simple analytics dashboard for admins/staff only."""
    today = timezone.localdate()
    week_end = today + timedelta(days=6)  # next 7 days including today

    # Today's bookings
    todays_bookings = Booking.objects.filter(date=today).order_by("time")

    # Pending confirmations
    pending_count = Booking.objects.filter(
        status=Booking.Status.PENDING
    ).count()

    # Bookings per day for last 7 days
    per_day = (
        Booking.objects
        .filter(date__range=[today, week_end])
        .values("date")
        .annotate(total=Count("id"))
        .order_by("date")
    )

    chart_labels = [b["date"].strftime("%Y-%m-%d") for b in per_day]
    chart_values = [b["total"] for b in per_day]
    chart_total = sum(chart_values)

    context = {
        "today": today,
        "todays_bookings": todays_bookings,
        "pending_count": pending_count,
        # send as JSON strings for Chart.js
        "chart_labels": json.dumps(chart_labels),
        "chart_values": json.dumps(chart_values),
        "chart_total": chart_total,
    }
    return render(request, "bookings/admin_dashboard.html", context)
