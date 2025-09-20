from django.shortcuts import render

# Create your views here.
# students/views.py
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Student, College
from rest_framework.permissions import AllowAny


class BulkUploadStudentsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        college_id = request.data.get("college_id")
        file = request.FILES.get("file")

        if not college_id or not file:
            return Response(
                {"error": "college_id and file are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            college = College.objects.get(id=college_id)
        except College.DoesNotExist:
            return Response({"error": "Invalid college_id."}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith(".csv"):
            return Response({"error": "File must be CSV."}, status=status.HTTP_400_BAD_REQUEST)

        data_set = file.read().decode("UTF-8")
        lines = data_set.splitlines()
        reader = csv.DictReader(lines)
        # print("="*80)
        # print(data_set)
        # print(lines)
        # print(reader)
        # print("="*80)

        created, updated = 0, 0
        errors = []

        for idx, row in enumerate(reader, start=1):
            try:
                obj, is_created = Student.objects.update_or_create(
                    email=row["email"].strip(),
                    defaults={
                        "name": row["name"].strip(),
                        "enrollment_no": row["enrollment_no"].strip(),
                        "college": college,
                        "batch": int(row["batch"]),
                        "department": row["department"].strip(),
                        "courses": eval(row["courses"]) if row["courses"] else [],
                    },
                )
                if is_created:
                    created += 1
                else:
                    updated += 1
            except Exception as e:
                errors.append({"row": idx, "error": str(e), "data": row})

        return Response(
            {
                "message": "Bulk upload completed",
                "created": created,
                "updated": updated,
                "errors": errors,
            },
            status=status.HTTP_201_CREATED,
        )


