
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.jwt_utils import *
import json
from ..models import *


@csrf_exempt
@token_required
def delete_academic_calendar_event(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can delete academic calendar" }, status=403)
        
        event_id = request.POST.get('calendar_event_id', '').strip()
        try:
            event = AdacemicCalendarEvent.objects.get(pk=event_id)
        except AdacemicCalendarEvent.DoesNotExist:
            return JsonResponse({ "error": "Adacemic Calendar Event not found" }, status=404)
        
        event.delete()
        return JsonResponse({ "message": "Adacemic Calendar Event deleted successfully" }, status=200)
    return JsonResponse({ "error": "Invalid request method" }, status=400)



@csrf_exempt
@token_required
def delete_news(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can delete news" }, status=403)
        
        news_id = request.POST.get('news_id', '').strip()
        try:
            news = News.objects.get(pk=news_id)
        except News.DoesNotExist:
            return JsonResponse({ "error": "News not found" }, status=404)
        
        news.delete()
        return JsonResponse({ "message": "News deleted successfully" }, status=200)
    return JsonResponse({ "error": "Invalid request method" }, status=400)



@csrf_exempt
@token_required
def delete_event(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can delete events" }, status=403)
        
        event_id = request.POST.get('event_id', '').strip()
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return JsonResponse({ "error": "Event not found" }, status=404)
        
        event.delete()
        return JsonResponse({ "message": "Event deleted successfully" }, status=200)
    return JsonResponse({ "error": "Invalid request method" }, status=400)