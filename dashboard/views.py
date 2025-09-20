import csv
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Student, College
from rest_framework.permissions import AllowAny

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
        return Response({"message": "Welcome to the University Dashboard!"}, status=status.HTTP_200_OK)

class BulkUploadStudentsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
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
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)