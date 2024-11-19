
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




# Request format for create_academic_calendar:
"""
POST at domain.com/api/create_academic_calendar/
{
    "events": [
        {
            "title": "Event 1",
            "start_date": "01-01-2022"
        },
        {
            "title": "Event 2",
            "start_date": "02-01-2022"
        }
    ]
}

"""


# Create academic calendar - TODO: INCLOMPLETE UNTIL STUDENT MODULE IS DONE
@csrf_exempt
@token_required
def create_academic_calendar(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can create academic calendar" }, status=403)
        
        data = json.loads(request.body)
        events_data = data.get('events', [])
        events = []
        for event_data in events_data:
            event = AdacemicCalendarEvent.objects.create(
                title=event_data.get('title', ''),
                start_date=datetime.strptime(event_data.get('start_date', ''), '%d-%m-%Y').date()
            )
            events.append(event)
        calendar = AcademicCalendar.objects.create()
        calendar.events.set(events)
        return JsonResponse({ "message": "Academic calendar created successfully" }, status=201)
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
                "created_at": news_item.created_at.strftime('%d-%m-%Y %H:%M'),
            })
        return JsonResponse({ "news": news_data }, status=200)





"""
Input format:
POST at domain.com/api/news/create/
{
    "title": "News Title",
    "content": "News content"
}
"""

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
        if not title or not content:
            return JsonResponse({ "error": "Title and content are required" }, status=400)
        
        news = News.objects.create(
            title=title,
            content=content
        )
        news.save()

        return JsonResponse({ "message": "News created successfully" }, status=201)
    return JsonResponse({ "error": "Invalid request" }, status=400)



@csrf_exempt
def get_events(request):
    if request.method == 'GET':
        events = Event.objects.all()
        events_data = []
        for activity in events:
            events_data.append({
                "title": activity.title,
                "image": activity.image.url,
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

