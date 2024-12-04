
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.jwt_utils import *
import json
from ..models import *



@csrf_exempt
@token_required
def edit_event(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can edit events" }, status=403)
        
        event_id = request.POST.get('event_id', '').strip()
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return JsonResponse({ "error": "Event not found" }, status=404)

        title = request.POST.get('title', '').strip()
        image = request.FILES.get('image', None)
        description = request.POST.get('description', '').strip()
        link = request.POST.get('link', '').strip()
        date = request.POST.get('date', '').strip()
        time = request.POST.get('time', '').strip()
        venue = request.POST.get('venue', '').strip()
        registration = request.POST.get('registration', '').strip()
        participation_registration = request.POST.get('participation_registration', '').strip()
        linkedin = request.POST.get('linkedin', '').strip()

        if title:
            event.title = title
        if image:
            event.image = image
        if description:
            event.description = description
        if link:
            event.link = link
        if date:
            event.date = datetime.strptime(date, '%d-%m-%Y')
        if time:
            event.time = datetime.strptime(time, '%H:%M')
        if venue:
            event.venue = venue
        if registration:
            event.registration = registration
        if participation_registration:
            event.participation_registration = participation_registration
        if linkedin:
            event.linkedin = linkedin

        event.save()

        return JsonResponse({ "message": "Event edited successfully" }, status=200)
    return JsonResponse({ "error": "Invalid request" }, status=400)














# Edit news by admin
@csrf_exempt
@token_required
def edit_news(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can edit news" }, status=403)
        
        news_id = request.POST.get('news_id', '').strip()
        try:
            news = News.objects.get(pk=news_id)
        except News.DoesNotExist:
            return JsonResponse({ "error": "News not found" }, status=404)

        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        youtube_link = request.POST.get('youtube_link', '').strip()
        image = request.FILES.get('image', None)

        if title:
            news.title = title
        if content:
            news.content = content
        if youtube_link:
            news.youtube_link = youtube_link
        if image:
            news.image = image

        news.save()

        return JsonResponse({ "message": "News edited successfully" }, status=200)
    return JsonResponse({ "error": "Invalid request method. It must be POST." }, status=400)












# Edit academic calendar event by admin
@csrf_exempt
@token_required
def edit_academic_calendar_event(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can edit academic calendar events" }, status=403)
        
        calendar_event_id = request.POST.get('calendar_event_id', '').strip()
        try:
            event = AdacemicCalendarEvent.objects.get(pk=calendar_event_id)
        except AdacemicCalendarEvent.DoesNotExist:
            return JsonResponse({ "error": "Academic calendar event not found" }, status=404)

        title = request.POST.get('title', '').strip()
        start_date = request.POST.get('start_date', '').strip()

        if title:
            event.title = title
        if start_date:
            event.start_date = datetime.strptime(start_date, '%d-%m-%Y')

        event.save()

        return JsonResponse({ "message": "Academic calendar event edited successfully" }, status=200)
    return JsonResponse({ "error": "Invalid request" }, status=400)
