from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.jwt_utils import *
import json
from .models import * # Custom user, not the default one



"""
POST at domain.com/api/signup/
{
    "username": "my_username",
    "password": "my_password"
}

OUTPUT:
{
    "message": "User created successfully"
}
    OR
{
    "error": "Username and password are required"
}
    OR
{
        "error": "Username already exists"
}
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError

@csrf_exempt
def signup(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()
    
    if not username or not password:
        return JsonResponse({"error": "Username and password are required"}, status=400)
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)
    
    try:
        with transaction.atomic():
            user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User created successfully"}, status=201)
    
    except IntegrityError:
        return JsonResponse({"error": "Username already exists"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)



        






"""
POST at domain.com/api/login/
{
    "username": "my_username",
    "password": "my_password"
}

OUTPUT:
{
    "token": "eyJ0eXAAAAAAAAAAAAAAAAAAAA"
}
    OR
{
    "error": "Invalid credentials"
}
"""

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            print(User.objects.all())
            user = User.objects.get(username=username)
            if user.check_password(password):  # Using check_password to verify
                token = create_jwt_token(user.username)
                return JsonResponse({"token": token}, status=200)
            else:
                return JsonResponse({"error": "Invalid password."}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does nto exist."}, status=401)
    return JsonResponse({"error": "Invalid request method."}, status=400)



# Geenral user data GET
@csrf_exempt
@token_required
def get_user(request):
    if request.method == 'GET':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        json_data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "admission_time": "--",
            "roll_number": "--",
            "program": "--",
            "cgpa": "--",
            "is_graduated": "--",
            "is_dropout": "--",

            "father_name":  "--",
            "father_occupation":  "--",
            "guardian_name":  "--",
            "guardian_occupation":  "--",
            "date_of_birth":  "--",
            "nic":  "--",
            "blood_group":  "--",
        }
        return JsonResponse(json_data, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)



# Student/faculty/admin specific logins

@csrf_exempt
def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user = User.objects.get(username=username)
            student = Student.objects.get(user=user)
            if user.check_password(password) and user.student:
                token = create_jwt_token(user.username)
                return JsonResponse({"token": token}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials."}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=401)
        except Student.DoesNotExist:
            return JsonResponse({"error": "User is not a student."}, status=401)
    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
def login_faculty(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user = User.objects.get(username=username)
            if not user.is_faculty:
                return JsonResponse({"error": "user is not a faculty."}, status=401)
            if user.check_password(password) and user.is_faculty:
                token = create_jwt_token(user.username)
                return JsonResponse({"token": token}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials."}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=401)
    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user = User.objects.get(username=username)
            if not user.is_superuser and not user.is_staff:
                return JsonResponse({"error": "user is not an admin."}, status=401)
            if user.check_password(password):
                token = create_jwt_token(user.username)
                return JsonResponse({"token": token}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials."}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=401)
    return JsonResponse({"error": "Invalid request method."}, status=400)