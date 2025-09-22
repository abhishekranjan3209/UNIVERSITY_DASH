from rest_framework import serializers
from .models import University, College, Course, Student, StudentEnrollemnt

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'

class CollegeSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    university_id = serializers.PrimaryKeyRelatedField(queryset=University.objects.all(), source='university', write_only=True)
    class Meta:
        model = College
        fields = ['id','name','metadata','university','university_id']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    college = CollegeSerializer(read_only=True)
    college_id = serializers.PrimaryKeyRelatedField(queryset=College.objects.all(), source='college', write_only=True)
    class Meta:
        model = Student
        fields = ['id','name','email','enrollement','batch','department','courses','college','college_id','created_at','updated_at']

class StudentEnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), source='student', write_only=True)
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source='course', write_only=True)
    class Meta:
        model = StudentEnrollemnt
        fields = ['id','student','student_id','course','course_id','created_at','updated_at','expiry_date','is_active','enrollement_id','product_type','enrollment_metadata']