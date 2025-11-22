from django.urls import path
from . import views

urlpatterns = [
    path("", views.booking_create, name="booking_create"),
    path("success/", views.booking_success, name="booking_success"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
