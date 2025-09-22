



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



# In admin.py

@admin.register(StudentEnrollemnt)
class StudentEnrollemntAdmin(admin.ModelAdmin):
    # We will now call our custom function 'get_course_name'
    list_display = ("enrollement_id", "student", "get_course_name", "is_active", "expiry_date")
    
    # The double-underscore lookup should still be used for searching
    search_fields = ("enrollement_id", "student__email", "course__name")

    # This is the new custom function
    @admin.display(description='Course Name', ordering='course__name')
    def get_course_name(self, obj):
        """Returns the name of the related course."""
        return obj.course.name