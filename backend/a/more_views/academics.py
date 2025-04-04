
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
                "calendar_event_id": event.pk,
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
                "news_id": news_item.pk,
                "title": news_item.title,
                "content": news_item.content,
                "youtube_link": news_item.youtube_link,
                "image": news_item.image.url,
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
        image = request.FILES.get('image', None)
        if not title or not content or not youtube_link or not image:
            return JsonResponse({ "error": "Title and content and yt link and image url is required" }, status=400)
        
        news = News.objects.create(
            title=title,
            content=content,
            youtube_link=youtube_link,
            image=image
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
                "event_id": activity.pk,
                "title": activity.title,
                "image": activity.image.url,
                "description": activity.description,
                "link": activity.link,
                "created_at": activity.created_at.strftime('%d-%m-%Y %H:%M'),
                "date": activity.date.strftime('%d-%m-%Y'),
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
        image = request.FILES.get('image', None)
        description = request.POST.get('description', '').strip()
        link = request.POST.get('link', '').strip()
        date = request.POST.get('date', '').strip()
        time = request.POST.get('time', '').strip()
        venue = request.POST.get('venue', '').strip()
        registration = request.POST.get('registration', '').strip()
        participation_registration = request.POST.get('participation_registration', '').strip()
        linkedin = request.POST.get('linkedin', '').strip()

        # convert date from dd-mm-yyyy into a date object
        date = datetime.strptime(date, '%d-%m-%Y')
        # convert time from hh:mm into a time object
        time = datetime.strptime(time, '%H:%M')

        event = Event.objects.create(
            title=title,
            image=image,
            description=description,
            link=link,
            date=date,
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
                "activity_id": activity.pk,
                "title": activity.title,
                "image": activity.image.url,
                "description": activity.description,
                "link": activity.link,
                "created_at": activity.created_at.strftime('%d-%m-%Y %H:%M'),
            })
        return JsonResponse({ "extracurricularactivities": activities_data }, status=200)
    return JsonResponse({ "error": "Invalid request" }, status=400)









@csrf_exempt
@token_required
def get_exam_time_tables(request):
    if request.method == 'GET':
        try:
            # Get the current student based on JWT token
            student = Student.objects.get(user__username=decode_jwt_token(request.headers.get('token')))
            
            # Get all exam timetables
            exam_timetables = ExamTimeTable.objects.all()
            exam_timetables_data = []
            
            for exam_timetable in exam_timetables:
                filtered_papers = []
                for exam_paper in exam_timetable.exam_papers.all():
                    # Check if this exam paper is for student's class
                    if exam_paper._class and exam_paper._class == student._class:
                        filtered_papers.append(exam_paper.get_json())
                    # Or check if the student is enrolled in this course through lectures
                    elif student.lectures.filter(course=exam_paper.course).exists():
                        filtered_papers.append(exam_paper.get_json())
                
                # Only add the timetable if it has papers for the student
                if filtered_papers:
                    exam_timetables_data.append({
                        "exam_papers": filtered_papers
                    })
            
            return JsonResponse({
                "exam_timetables": exam_timetables_data,
                "student_class": student._class.name if student._class else None
            }, status=200)
            
        except Student.DoesNotExist:
            return JsonResponse({
                "error": "Student not found"
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=500)
    
    return JsonResponse({
        "error": "Invalid request"
    }, status=400)