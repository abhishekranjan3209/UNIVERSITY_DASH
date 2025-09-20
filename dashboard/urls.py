# students/urls.py
from django.urls import path
from .views import BulkUploadStudentsView

urlpatterns = [
    path("bulk-upload/", BulkUploadStudentsView.as_view(), name="bulk-upload-students"),
]