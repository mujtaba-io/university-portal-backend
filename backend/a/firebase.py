
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.jwt_utils import *
import json
from .models import *


import firebase_admin
from firebase_admin import credentials, messaging

# import base dir
import os
from pathlib import Path


# In prod (hf spaces) as a secret in env:
serviceAccountKeyJSON = os.getenv('firebase_maju_trackmate_service_account') # secret in hf space env
if serviceAccountKeyJSON:
    # convert it to a dict
    serviceAccountKey = json.loads(serviceAccountKeyJSON)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    # As a file, as in local
    serviceAccountKey = os.path.join(BASE_DIR, 'secrets/maju-trackmate-firebase-adminsdk-77k2f-0756d0c2cb.json')


# Path to your Firebase service account key JSON file
cred = credentials.Certificate(serviceAccountKey)
firebase_admin.initialize_app(cred)






# Send notifs - API, to send push notifications to a single device
from firebase_admin import messaging

def send_push_notification(token, title, body, data=None):
    """
    Sends a push notification to a single device using FCM.
    
    Args:
        token (str): FCM device token.
        title (str): Notification title.
        body (str): Notification body.
        data (dict, optional): Additional data payload.
    """
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
            data=data if data else {}
        )
        response = messaging.send(message)
        print(f"Notification sent successfully: {response}")
    except Exception as e:
        print(f"Error sending notification: {e}")









# Register token sent for each user, by the frontend
@csrf_exempt
@token_required
def register_fcm_token(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if user:
            device_fcm_token = request.POST.get('device_fcm_token')
            user.device_fcm_token = device_fcm_token
            user.save()

            # If token registered successfully, send a test notification
            send_push_notification(
                token=device_fcm_token,
                title="HEHE FCM Token Registered",
                body="You will now receive notifications from Maju Trackmate"
            )
            return JsonResponse({"message": "FCM token registered successfully"}, status=200)
        return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)



