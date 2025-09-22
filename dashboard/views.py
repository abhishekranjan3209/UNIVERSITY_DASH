import csv, io
from datetime import date
import json
from django.db import transaction, models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import University, College, Course, Student, StudentEnrollemnt
from .serializers import (
    UniversitySerializer,
    CollegeSerializer,
    CourseSerializer,
    StudentSerializer,
    StudentEnrollmentSerializer,
)
def get_user_data_for_rest_api(request_data):
    user_data = request_data.get('user_data')
    user_data = json.loads(user_data)
    return user_data


class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        user_data = get_user_data_for_rest_api(request_data)
        user_permissions = user_data.get('user_permission')
        print("=== Incoming Request ===")
        print("User Data:", user_data)
        print("User Permissions:", user_permissions)
        print("========================")
        return Response({"message": "Welcome to the University Dashboard! sab sahi chal reha h"}, status=status.HTTP_200_OK)
# ----------------- role-based scope helper -----------------

def checkuser(request, qs):
    profile = getattr(request.user, "profile", None)
    if not profile:
        return qs.none()

    if profile.role == "UNIVERSITY" and profile.university:
        if qs.model is Student:
            return qs.filter(college__university=profile.university)
        if qs.model is StudentEnrollemnt:
            return qs.filter(student__college__university=profile.university)
        if qs.model is College:
            return qs.filter(university=profile.university)

    if profile.role == "COLLEGE" and profile.college:
        if qs.model is Student:
            return qs.filter(college=profile.college)
        if qs.model is StudentEnrollemnt:
            return qs.filter(student__college=profile.college)
        if qs.model is College:
            return qs.filter(id=profile.college_id)

    return qs

# ----------------- Universities -----------------

class UniversityListCreateView(APIView):
#    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = University.objects.all()
        #qs = checkuser(request, qs)
        serializer = UniversitySerializer(qs, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = UniversitySerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=201)


class UniversityDetailView(APIView):
#    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        qs = checkuser(request, University.objects.all())
        return get_object_or_404(qs, pk=pk)

    def get(self, request, pk):
        obj = self.get_object(request, pk)
        return Response(UniversitySerializer(obj).data)

    def put(self, request, pk):
        obj = self.get_object(request, pk)
        s = UniversitySerializer(obj, data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)

    def delete(self, request, pk):
        profile = getattr(request.user, "profile", None)
        if not profile or profile.role != "ADMIN":
            return Response({"detail": "Only ADMIN can delete"}, status=403)
        obj = self.get_object(request, pk)
        obj.delete()
        return Response(status=204)

# ----------------- Colleges -----------------

class CollegeListCreateView(APIView):
#    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = College.objects.select_related("university").all()
        #qs = checkuser(request, qs)
        # filter by university (optional)
        uni = request.GET.get("university")
        if uni:
            qs = qs.filter(university=uni)
        return Response(CollegeSerializer(qs, many=True).data)

    # def post(self, request):
    #     s = CollegeSerializer(data=request.data)
    #     s.is_valid(raise_exception=True)
    #     s.save()
    #     return Response(s.data, status=201)


class CollegeDetailView(APIView):
#    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        qs = checkuser(request, College.objects.all())
        return get_object_or_404(qs, pk=pk)

    def get(self, request, pk):
        obj = self.get_object(request, pk)
        return Response(CollegeSerializer(obj).data)

    def put(self, request, pk):
        obj = self.get_object(request, pk)
        s = CollegeSerializer(obj, data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)

    def delete(self, request, pk):
        profile = getattr(request.user, "profile", None)
        if not profile or profile.role != "ADMIN":
            return Response({"detail": "Only ADMIN can delete"}, status=403)
        obj = self.get_object(request, pk)
        obj.delete()
        return Response(status=204)

# ----------------- Courses -----------------

class CourseListCreateView(APIView):
#    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Course.objects.all()
        return Response(CourseSerializer(qs, many=True).data)

    # def post(self, request):
    #     s = CourseSerializer(data=request.data)
    #     s.is_valid(raise_exception=True)
    #     s.save()
    #     return Response(s.data, status=201)


class CourseDetailView(APIView):
#    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        obj = get_object_or_404(Course.objects.all(), pk=pk)
        return Response(CourseSerializer(obj).data)

    def put(self, request, pk):
        obj = get_object_or_404(Course.objects.all(), pk=pk)
        s = CourseSerializer(obj, data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)

    def delete(self, request, pk):
        obj = get_object_or_404(Course.objects.all(), pk=pk)
        obj.delete()
        return Response(status=204)

# ----------------- Students -----------------

class StudentListCreateView(APIView):
#    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Student.objects.select_related("college", "college__university").all()
        #qs = checkuser(request, qs)

        # lightweight filters
        college = request.GET.get("college")
        uni = request.GET.get("college__university")
        batch = request.GET.get("batch")
        dept = request.GET.get("department")
        if college:
            qs = qs.filter(college=college)
        if uni:
            qs = qs.filter(college__university=uni)
        if batch:
            qs = qs.filter(batch=batch)
        if dept:
            qs = qs.filter(department=dept)

        return Response(StudentSerializer(qs, many=True).data)

    # def post(self, request):
    #     s = StudentSerializer(data=request.data)
    #     s.is_valid(raise_exception=True)
    #     s.save()
    #     return Response(s.data, status=201)


class StudentDetailView(APIView):
#    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        qs = checkuser(request, Student.objects.all())
        return get_object_or_404(qs, pk=pk)

    def get(self, request, pk):
        obj = self.get_object(request, pk)
        return Response(StudentSerializer(obj).data)

    def put(self, request, pk):
        obj = self.get_object(request, pk)
        s = StudentSerializer(obj, data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)

    def delete(self, request, pk):
        profile = getattr(request.user, "profile", None)
        if not profile or profile.role != "ADMIN":
            return Response({"detail": "Only ADMIN can delete"}, status=403)
        obj = self.get_object(request, pk)
        obj.delete()
        return Response(status=204)

# ----------------- Enrollments -----------------

class EnrollmentListCreateView(APIView):
#    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = StudentEnrollemnt.objects.select_related(
            "student", "course", "student__college", "student__college__university"
        ).all()
        qs = checkuser(request, qs)

        # filters
        student = request.GET.get("student")
        course = request.GET.get("course")
        is_active = request.GET.get("is_active")
        college = request.GET.get("student__college")
        uni = request.GET.get("student__college__university")

        if student:
            qs = qs.filter(student=student)
        if course:
            qs = qs.filter(course=course)
        if is_active in ("true", "false", "1", "0"):
            qs = qs.filter(is_active=is_active in ("true", "1"))
        if college:
            qs = qs.filter(student__college=college)
        if uni:
            qs = qs.filter(student__college__university=uni)

        return Response(StudentEnrollmentSerializer(qs, many=True).data)

    # def post(self, request):
    #     s = StudentEnrollmentSerializer(data=request.data)
    #     s.is_valid(raise_exception=True)
    #     s.save()
    #     return Response(s.data, status=201)


class EnrollmentDetailView(APIView):
#    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        qs = checkuser(request, StudentEnrollemnt.objects.all())
        return get_object_or_404(qs, pk=pk)

    def get(self, request, pk):
        obj = self.get_object(request, pk)
        return Response(StudentEnrollmentSerializer(obj).data)

    def put(self, request, pk):
        obj = self.get_object(request, pk)
        s = StudentEnrollmentSerializer(obj, data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)

    def delete(self, request, pk):
        profile = getattr(request.user, "profile", None)
        if not profile or profile.role != "ADMIN":
            return Response({"detail": "Only ADMIN can delete"}, status=403)
        obj = self.get_object(request, pk)
        obj.delete()
        return Response(status=204)

# ----------------- Extra endpoints -----------------
import io, csv
from datetime import datetime, date
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student, College, University, Course, StudentEnrollemnt

class StudentBulkUploadView(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        course_ids = request.data.getlist("course_ids")
        start = request.data.get("start_date")
        end = request.data.get("end_date")

        if not file:
            return Response({"detail": "CSV file required"}, status=400)

        try:
            data = file.read().decode("utf-8")
        except UnicodeDecodeError:
            return Response({"detail": "CSV must be UTF-8 text"}, status=400)

        f = io.StringIO(data)
        reader = csv.DictReader(f)

        # Handle courses
        courses = []
        invalid_ids = []
        # for cid in course_ids:
        #     try:
        #         courses.append(Course.objects.get(pk=cid))
        #     except Course.DoesNotExist:
        #         invalid_ids.append(cid)
        # if invalid_ids:
        #     return Response({"detail": f"Invalid course_ids: {invalid_ids}"}, status=400)

        created, updated = 0, 0
        today = date.today()

        with transaction.atomic():
            for row in reader:
                uni_name = row.get("university")
                col_name = row.get("college")
                u, _ = University.objects.get_or_create(name=uni_name)
                c, _ = College.objects.get_or_create(university=u, name=col_name)

                student, was_created = Student.objects.update_or_create(
                    email=row["email"],
                    defaults={
                        "name": row.get("name", ""),
                        "enrollement": int(row.get("enrollement") or 0),
                        "batch": int(row.get("batch") or 0),
                        "department": row.get("department", ""),
                        "college": c,
                    },
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

                # for course in courses:
                #     expiry_date = datetime.strptime(end, "%Y-%m-%d").date() if end else today
                #     StudentEnrollemnt.objects.get_or_create(
                #         student=student,
                #         course=course,
                #         defaults={
                #             "expiry_date": expiry_date,
                #             "is_active": True,
                #             "enrollement_id": f"{student.id}-{course.id}-{today.isoformat()}",
                #             "product_type": "COURSE",
                #             "enrollment_metadata": {"start_date": start, "end_date": end},
                #         },
                #     )

        return Response({"created": created, "updated": updated})

# class StudentBulkUploadView(APIView):
#     """
#     POST form-data:
#       - file: CSV (name,email,enrollement,university,college,batch,department)
#       - course_ids: can repeat (e.g., 1, 2, 3)
#       - start_date: YYYY-MM-DD (optional)
#       - end_date:   YYYY-MM-DD (optional)
#     Only ADMIN can call.
#     """
# #    permission_classes = [IsAuthenticated]

#     def post(self, request):
#         # profile = getattr(request.user, "profile", None)
#         # if not profile or profile.role != "ADMIN":
#         #     return Response({"detail": "Only ADMIN can upload CSV."}, status=403)

#         file = request.FILES.get("file")
#         course_ids = request.data.getlist("course_ids")
#         start = request.data.get("start_date")
#         end = request.data.get("end_date")

#         if not file:
#             return Response({"detail": "CSV file required"}, status=400)
#         # if not course_ids:
#         #     return Response({"detail": "At least one course_ids required"}, status=400)

#         try:
#             data = file.read().decode("utf-8")
#         except UnicodeDecodeError:
#             return Response({"detail": "CSV must be UTF-8 text"}, status=400)

#         f = io.StringIO(data)
#         reader = csv.DictReader(f)

#         # prefetch courses
#         try:
#             courses = [Course.objects.get(pk=cid) for cid in course_ids]
#         except Course.DoesNotExist:
#             return Response({"detail": f"Invalid course_ids: {course_ids}"}, status=400)

#         created, updated = 0, 0
#         today = date.today()

#         with transaction.atomic():
#             for row in reader:
#                 uni_name = row.get("university")
#                 col_name = row.get("college")
#                 u, _ = University.objects.get_or_create(name=uni_name)
#                 c, _ = College.objects.get_or_create(university=u, name=col_name)

#                 student, was_created = Student.objects.update_or_create(
#                     email=row["email"],
#                     defaults={
#                         "name": row.get("name", ""),
#                         "enrollement": int(row.get("enrollement") or 0),
#                         "batch": int(row.get("batch") or 0),
#                         "department": row.get("department", ""),
#                         "college": c,
#                     },
#                 )
#                 if was_created:
#                     created += 1
#                 else:
#                     updated += 1

#                 for course in courses:
#                     StudentEnrollemnt.objects.get_or_create(
#                         student=student,
#                         course=course,
#                         defaults={
#                             "expiry_date": end or today,
#                             "is_active": True,
#                             "enrollement_id": f"{student.id}-{course.id}-{today.isoformat()}",
#                             "product_type": "COURSE",
#                             "enrollment_metadata": {"start_date": start, "end_date": end},
#                             #"progress_percent": 0,
#                         },
#                     )

#         return Response({"created": created, "updated": updated})
    







    

# #bewlo class is for like if college want to download all the students details so can download from this 

# # class StudentExportCSVView(APIView):
# #     """
# #     GET with optional filters: college, college__university, batch, department
# #     """
# # #    permission_classes = [IsAuthenticated]

# #     def get(self, request):
# #         qs = Student.objects.select_related("college", "college__university").all()
# #         qs = checkuser(request, qs)

# #         college = request.GET.get("college")
# #         uni = request.GET.get("college__university")
# #         batch = request.GET.get("batch")
# #         dept = request.GET.get("department")

# #         if college:
# #             qs = qs.filter(college=college)
# #         if uni:
# #             qs = qs.filter(college__university=uni)
# #         if batch:
# #             qs = qs.filter(batch=batch)
# #         if dept:
# #             qs = qs.filter(department=dept)

# #         resp = HttpResponse(content_type="text/csv")
# #         resp["Content-Disposition"] = 'attachment; filename="students.csv"'
# #         w = csv.writer(resp)
# #         w.writerow(["name", "email", "enrollement", "college", "university", "batch", "department"])
# #         for s in qs:
# #             w.writerow([s.name, s.email, s.enrollement, s.college.name, s.college.university.name, s.batch, s.department])
# #         return resp


