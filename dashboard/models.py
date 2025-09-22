from django.db import models


from django.db.models import JSONField
from django.contrib.auth import get_user_model

User = get_user_model()



class University(models.Model):
    """
    Represents a university entity.

    Fields:
        name (CharField): The name of the university. Maximum length is 200 characters.
        metadata (JSONField): Optional field to store additional information about
            the university in JSON format. Defaults to an empty dictionary.

    Methods:
        __str__: Returns the string representation of the university, which is its name.
    """
    name=models.CharField(max_length=200)
    metadata = models.JSONField(default=dict, blank=True)
    def __str__(self):
        return self.name
    

class College(models.Model):
    """
    Represents a college that belongs to a university.

    Fields:
        university (ForeignKey): A reference to the related University. 
            If the university is deleted, all associated colleges are deleted (CASCADE).
        name (CharField): The name of the college. Maximum length is 200 characters.
        metadata (JSONField): Optional field to store additional information 
            about the college in JSON format. Defaults to an empty dictionary.

    Methods:
        __str__: Returns the string representation of the college, which is its name.
    """
    university=models.ForeignKey(University, on_delete=models.CASCADE, related_name="colleges")
    name= models.CharField(max_length=200)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    """
    Represents a student enrolled in a college.

    Fields:
        name (CharField): The full name of the student. Maximum length is 200 characters.
        email (EmailField): The unique email address of the student. Indexed for faster lookups.
        enrollement (IntegerField): The enrollment number assigned to the student.

        college (ForeignKey): A reference to the related College. 
        -If the college is deleted, all associated students are deleted (CASCADE).

        batch (IntegerField): The passing batch year (e.g., 2025).

        department (CharField): The department of the student (e.g., Computer Science).

        courses (JSONField): A JSON field storing the list of courses the student is enrolled in.

        created_at (DateTimeField): Timestamp when the student record was created. 
            Automatically set and not editable.

        updated_at (DateTimeField): Timestamp when the student record was last updated. 
            Automatically updated on save.

    Methods:
        __str__: Returns the string representation of the student, which is their email.
    """
    name= models.CharField(max_length=200)
    email= models.EmailField(unique=True, db_index=True)
    enrollement=models.IntegerField() # given enrollment no 

    college= models.ForeignKey(College, on_delete=models.CASCADE, related_name="students")
    batch= models.IntegerField() #2025
    department= models.CharField(max_length=200) #computer science
    courses = JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):

        return self.email
    
class Course(models.Model):
    course_id = models.CharField(max_length=100, db_index=True)
    name = models.CharField(max_length=200)
    metadata = models.JSONField(default=dict, blank=True)
    # In models.py > class Course
    def __str__(self):
        return self.name
      
      
      


class StudentEnrollemnt(models.Model):
    """
    Represents a student's enrollment in a specific course or program.

    Fields:
        student (ForeignKey): A reference to the related Student. 
            If the student is deleted, their enrollments are also deleted (CASCADE).
        course_id (IntegerField): The unique identifier of the course.

        course_name (CharField): The name of the course. Maximum length is 200 characters.

        created_at (DateTimeField): Timestamp when the enrollment record was created. 
            Automatically set and not editable.

        updated_at (DateTimeField): Timestamp when the enrollment record was last updated. 
            Automatically updated on save.

        expiry_date (DateField): The date when the enrollment expires.
        is_active (BooleanField): Status flag indicating whether the enrollment is currently active.

        enrollement_id (CharField): A unique identifier for the enrollment. 
            Indexed for faster lookups.

        product_type (CharField): Specifies whether the enrollment is for a "COURSE" or a "PROGRAM".

        enrollment_metadata (JSONField): Optional field for storing additional metadata 
            about the enrollment in JSON format.

    Methods:
        __str__: Returns the string representation of the enrollment, which is the student's name.
    """
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')

    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    updated_at=models.DateTimeField(auto_now=True, editable=False)
    expiry_date=models.DateField()
    is_active = models.BooleanField(default=True)#is_active

    enrollement_id = models.CharField(max_length=100, unique=True, db_index=True)#enrollement_id
    product_type = models.CharField(max_length=50, choices=[("COURSE", "Course"), ("PROGRAM", "Program")]) #product_type
    enrollment_metadata = models.JSONField(default=dict, blank=True)#enrollment_metadata

    def __str__(self):
        return self.student.email
    
#done till now

#need to ask if required to aDD THEN ADD ??????????????

class UserProfile(models.Model):
    ROLE_CHOICES = (('ADMIN','Admin'),('UNIVERSITY','University'),('COLLEGE','College'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    university = models.ForeignKey(University, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    college = models.ForeignKey(College, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    def __str__(self):
        return f"{self.user.username} ({self.role})"