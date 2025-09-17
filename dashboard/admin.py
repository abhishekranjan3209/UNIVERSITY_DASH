from django.contrib import admin
from .models import University, College, Student, StudentEnrollemnt

admin.site.register(University)
admin.site.register(College)
admin.site.register(Student)
admin.site.register(StudentEnrollemnt)
