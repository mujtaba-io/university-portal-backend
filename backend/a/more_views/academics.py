
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.jwt_utils import *
import json
from ..models import *


@csrf_exempt
@token_required
def get_academic_calendar(request):
    if request.method == 'GET':
        # get latest academic calendar
        calendar = AcademicCalendar.objects.latest('created_at')
        events = calendar.events.all()
        events_data = []
        for event in events:
            events_data.append({
                "title": event.title,
                "start_date": event.start_date.strftime('%d-%m-%Y'),
            })
        return JsonResponse(
            {
                "semester": calendar.semester_name,
                "calendar": events_data,
                },
            status=200
        )





# Create academic calendar event by admin
@csrf_exempt
@token_required
def add_academic_calendar_event(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can create academic calendar" }, status=403)
        
        semester_name = request.POST.get('semester_name', '').strip()
        title = request.POST.get('title', '').strip()
        start_date = request.POST.get('start_date', '').strip()

        # make start date a date object
        start_date = datetime.strptime(start_date, '%d-%m-%Y')

        if not semester_name or not title or not start_date:
            return JsonResponse({ "error": "Semester name, title and start date are required" }, status=400)

        # If academic calendar already exists, add event to it, else create a new one
        academic_calendar, is_created = AcademicCalendar.objects.get_or_create(semester_name=semester_name)
        if not academic_calendar:
            academic_calendar = AcademicCalendar.objects.create(semester_name=semester_name)
            academic_calendar.save()

        event = AdacemicCalendarEvent.objects.create(
            title=title,
            start_date=start_date
        )
        event.save()
        academic_calendar.events.add(event)
        academic_calendar.save()

        return JsonResponse({ "message": "Event added to academic calendar" }, status=201)
    return JsonResponse({ "error": "Invalid request" }, status=400)






"""
GET at domain.com/api/news/
"""

@csrf_exempt
# Token NOT required
def get_news(request):
    if request.method == 'GET':
        news = News.objects.all()
        news_data = []
        for news_item in news:
            news_data.append({
                "title": news_item.title,
                "content": news_item.content,
                "youtube_link": news_item.youtube_link,
                "image_url": news_item.image_url,
                "created_at": news_item.created_at.strftime('%d-%m-%Y %H:%M'),
            })
        return JsonResponse({ "news": news_data }, status=200)






# Create news by admin
@csrf_exempt
@token_required
def create_news(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can create news" }, status=403)
        
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        youtube_link = request.POST.get('youtube_link', '').strip()
        image_url = request.POST.get('image_url', '').strip()
        if not title or not content or not youtube_link or not image_url:
            return JsonResponse({ "error": "Title and content and yt link and image url is required" }, status=400)
        
        news = News.objects.create(
            title=title,
            content=content,
            youtube_link=youtube_link,
            image_url=image_url
        )
        news.save()

        return JsonResponse({ "message": "News created successfully" }, status=201)
    return JsonResponse({ "error": "Invalid request method. it must be POST." }, status=400)






@csrf_exempt
def get_events(request):
    if request.method == 'GET':
        events = Event.objects.all()
        events_data = []
        for activity in events:
            events_data.append({
                "title": activity.title,
                "image_url": activity.image_url,
                "description": activity.description,
                "link": activity.link,
                "created_at": activity.created_at.strftime('%d-%m-%Y %H:%M'),
                "day": activity.day,
                "time": activity.time.strftime('%H:%M'),
                "venue": activity.venue,
                "registration": activity.registration,
                "participation_registration": activity.participation_registration,
                "linkedin": activity.linkedin,
            })
        return JsonResponse({ "events": events_data }, status=200)
    return JsonResponse({ "error": "Invalid request" }, status=400)



@csrf_exempt
@token_required
def create_event(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can create events" }, status=403)
        
        title = request.POST.get('title', '').strip()
        image_url = request.FILES.get('image_url', None)
        description = request.POST.get('description', '').strip()
        link = request.POST.get('link', '').strip()
        day = request.POST.get('day', '').strip()
        time = request.POST.get('time', '').strip()
        venue = request.POST.get('venue', '').strip()
        registration = request.POST.get('registration', '').strip()
        participation_registration = request.POST.get('participation_registration', '').strip()
        linkedin = request.POST.get('linkedin', '').strip()

        if not title or not image_url or not description or not link or not day or not time or not venue or not registration or not participation_registration or not linkedin:
            return JsonResponse({ "error": "All fields are required" }, status=400)

        event = Event.objects.create(
            title=title,
            image_url=image_url,
            description=description,
            link=link,
            day=day,
            time=time,
            venue=venue,
            registration=registration,
            participation_registration=participation_registration,
            linkedin=linkedin
        )
        event.save()

        return JsonResponse({ "message": "Event created successfully" }, status=201)
    return JsonResponse({ "error": "Invalid request" }, status=400)











@csrf_exempt
def get_extra_curricular_activities(request):
    if request.method == 'GET':
        activities = ExtraCurricularActivity.objects.all()
        activities_data = []
        for activity in activities:
            activities_data.append({
                "title": activity.title,
                "image": activity.image.url,
                "description": activity.description,
                "link": activity.link,
                "created_at": activity.created_at.strftime('%d-%m-%Y %H:%M'),
            })
        return JsonResponse({ "extracurricularactivities": activities_data }, status=200)
    return JsonResponse({ "error": "Invalid request" }, status=400)

