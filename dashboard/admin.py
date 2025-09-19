from django.contrib import admin
from .models import University, College, Student, StudentEnrollemnt

# admin.site.register(University)
# admin.site.register(College)
# admin.site.register(Student)
# admin.site.register(StudentEnrollemnt)


from django.contrib import admin
from .models import University, College, Student, StudentEnrollemnt

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "university")

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "college", "batch", "department")
    search_fields = ("name", "email", "enrollement")

@admin.register(StudentEnrollemnt)
class StudentEnrollemntAdmin(admin.ModelAdmin):
    list_display = ("enrollement_id", "student", "course_name", "is_active", "expiry_date")
    search_fields = ("enrollement_id", "student__email", "course_name")
