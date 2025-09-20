# students/urls.py
from django.urls import path
from .views import BulkUploadStudentsView, DashboardView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("bulk-upload/", BulkUploadStudentsView.as_view(), name="bulk-upload-students"),
]