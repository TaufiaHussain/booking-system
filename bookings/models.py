from django.db import models


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    date = models.DateField()
    time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} – {self.date} {self.time} ({self.status})"


class EmailTemplate(models.Model):
    """
    Stores editable email templates in the DB.

    Example keys:
      - booking_received
      - new_booking_admin
      - booking_confirmed
    """

    key = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=200)
    body = models.TextField(
        help_text="You can use {{ booking.name }}, {{ booking.date }}, {{ booking.time }}, etc."
    )
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key} – {self.subject}"
