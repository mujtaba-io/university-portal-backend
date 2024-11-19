from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.jwt_utils import *
import json
from .models import User # Custom user, not the default one



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
            user = User.objects.get(username=username)
            if user.check_password(password):  # Using check_password to verify
                token = create_jwt_token(user.username)
                return JsonResponse({"token": token}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    return JsonResponse({"error": "Invalid request"}, status=400)
