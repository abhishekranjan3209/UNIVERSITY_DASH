from django.contrib import admin
from .models import University, College, Student, StudentEnrollment


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "university")
    search_fields = ("name", "university__name")
    list_filter = ("university",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "enrollment_no", "college", "batch", "department")
    search_fields = ("name", "email", "enrollment_no")
    list_filter = ("college", "batch", "department")


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "course_id", "course_name", "expiry_date", "created_at")
    search_fields = ("student__name", "student__email", "course_name")
    list_filter = ("expiry_date", "course_name")
