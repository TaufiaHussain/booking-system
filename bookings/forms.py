from django import forms
from django.utils import timezone
import datetime as dt

from .models import Booking


class DateInput(forms.DateInput):
    input_type = "date"


class TimeInput(forms.TimeInput):
    input_type = "time"


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["name", "email", "phone", "date", "time"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm",
                    "placeholder": "Your full name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm",
                    "placeholder": "you@example.com",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm",
                    "placeholder": "+49 ...",
                }
            ),
            "date": DateInput(
                attrs={
                    "class": "block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm",
                    # simple client-side guard; server-side rules are below
                    "min": dt.date.today().isoformat(),
                }
            ),
            "time": TimeInput(
                attrs={
                    "class": "block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time_value = cleaned_data.get("time")

        if not date or not time_value:
            return cleaned_data

        # ---- Combine into datetime in current timezone
        booking_dt = dt.datetime.combine(date, time_value)
        if timezone.is_naive(booking_dt):
            booking_dt = timezone.make_aware(
                booking_dt,
                timezone.get_current_timezone(),
            )

        now = timezone.now()

        # 1) No past bookings
        if booking_dt < now:
            raise forms.ValidationError(
                "You cannot book an appointment in the past."
            )

        # 2) No Sundays (weekday: Monday=0, Sunday=6)
        if date.weekday() == 6:
            raise forms.ValidationError(
                "Bookings are not available on Sundays."
            )

        # 3) Working hours 09:00–18:00 (18:00 excluded)
        OPEN_HOUR = 9
        CLOSE_HOUR = 18
        if time_value.hour < OPEN_HOUR or time_value.hour >= CLOSE_HOUR:
            raise forms.ValidationError(
                "Bookings are only possible between 09:00 and 18:00."
            )

        # 4) No double booking for same date+time (unless cancelled)
        qs = (
            Booking.objects
            .filter(date=date, time=time_value)
            .exclude(status=Booking.Status.CANCELLED)
        )
        # Ignore the current instance if editing later
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "This time slot is already booked. Please choose another time."
            )

        return cleaned_data
