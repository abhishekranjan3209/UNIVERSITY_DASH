from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UniversityViewSet, CollegeViewSet, CourseViewSet,
    StudentViewSet, EnrollmentViewSet,
    StudentBulkUploadView, StudentExportCSVView, EnrollmentProgressSummaryView
)

router = DefaultRouter()
router.register('universities', UniversityViewSet)
router.register('colleges', CollegeViewSet)
router.register('courses', CourseViewSet)
router.register('students', StudentViewSet, basename='students')
router.register('enrollments', EnrollmentViewSet, basename='enrollments')

urlpatterns = [
    path('', include(router.urls)),  # all CRUD from ViewSets auto-added

    # extra custom endpoints
    path('students/bulk-upload/', StudentBulkUploadView.as_view(), name='student-bulk-upload'),
    path('students/export-csv/', StudentExportCSVView.as_view(), name='student-export-csv'),
    path('enrollments/progress-summary/', EnrollmentProgressSummaryView.as_view(), name='enrollment-progress-summary'),
]