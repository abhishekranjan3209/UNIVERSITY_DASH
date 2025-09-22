from django.urls import path
from .views import (
    UniversityListCreateView, UniversityDetailView,
    CollegeListCreateView,    CollegeDetailView,
    CourseListCreateView,     CourseDetailView,
    StudentListCreateView,    StudentDetailView,
    EnrollmentListCreateView, EnrollmentDetailView,
    StudentBulkUploadView,    
    
)

urlpatterns = [
    # Universities
    path('universities/', UniversityListCreateView.as_view(), name='university-list'),
    path('universities/<int:pk>/', UniversityDetailView.as_view(), name='university-detail'),

    # Colleges
    path('colleges/', CollegeListCreateView.as_view(), name='college-list'),
    path('colleges/<int:pk>/', CollegeDetailView.as_view(), name='college-detail'),

    # Courses
    path('courses/', CourseListCreateView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    # Students
    path('students/', StudentListCreateView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('students/bulk-upload/', StudentBulkUploadView.as_view(), name='student-bulk-upload'),
   

    # Enrollments
    path('enrollments/', EnrollmentListCreateView.as_view(), name='enrollment-list'),
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
 
]