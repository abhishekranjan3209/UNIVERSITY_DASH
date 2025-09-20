from django.db import models
from django.db.models import JSONField


class University(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
    

class College(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="colleges")
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, db_index=True)
    enrollment_no = models.CharField(max_length=50, unique=True)  
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="students")
    batch = models.IntegerField()
    department = models.CharField(max_length=200)
    courses = JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.email


class StudentEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course_id = models.IntegerField()
    course_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    expiry_date = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.course_name}"
