from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.jwt_utils import *
import json
from ..models import *


# Faculty related views

# Endpoint for requesting a makeup lecture

@csrf_exempt
@token_required
def request_makeup_lecture(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)

        if not user.is_faculty:
            return JsonResponse({ "error": "Only faculty can request a makeup lecture" }, status=403)
        
        class_name = request.POST.get('class_name', '').strip()
        course_code = request.POST.get('course_code', '').strip()

        day = request.POST.get('day', '').strip()

        block_name = request.POST.get('block_name', '').strip()
        room_name = request.POST.get('room_name', '').strip()

        start_time = request.POST.get('start_time', '').strip()
        end_time = request.POST.get('end_time', '').strip()

        if not class_name or not course_code or not teacher_username or not day or not block_name or not room_name or not start_time or not end_time:
            return JsonResponse({ "error": "All fields are required" }, status=400)
        
        # check if teacher exists
        try:
            _class = Class.objects.get(name=class_name)
            course = Course.objects.get(code=course_code)
            block = Block.objects.get(name=block_name)
            room = Room.objects.get(name=room_name, block=block)
        except:
            return JsonResponse({ "error": "Invalid data provided" }, status=400)
        
        # Create a lectureobject
        lecture = Lecture.objects.create(
            class_name=_class,
            course=course,
            teacher=user, # This user is a faculty
            day=day,
            block=block,
            room=room,
            start_time=start_time,
            end_time=end_time,
            is_makeup=True # This is a makeup lecture
        )

        lecture.save()

        return JsonResponse({ "message": "Makeup lecture requested successfully" }, status=201)
    return JsonResponse({ "error": "Invalid request method" }, status=400)



# Endpoint to get all of the teacher's lectures
@csrf_exempt
@token_required
def faculty_time_table(request):
    if request.method == 'GET':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if user.is_faculty:
            # Get the lectures of the faculty
            this_teacher_lectures = Lecture.objects.filter(teacher=user)
            lectures_data = []
            for lecture in this_teacher_lectures:
                lectures_data.append({
                    "lecture_id": lecture.pk,
                    "course_name": lecture.course.name,
                    "course_code": lecture.course.code,
                    "class_name": lecture._class.name,
                    "day": lecture.day,
                    "room": lecture.room.name,
                    "start_time": lecture.start_time.strftime('%H:%M'),
                    "end_time": lecture.end_time.strftime('%H:%M'),
                })
            return JsonResponse({ "timetable": lectures_data }, status=200)
        return JsonResponse({"error": "Faculty not found"}, status=404)
    
    return JsonResponse({"error": "Invalid request"}, status=400)


# Endpoint to return all the students in a given lecture
@csrf_exempt
@token_required
def get_students_in_lecture(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)

        lecture_id = request.POST.get('lecture_id', '').strip()
        if not lecture_id:
            return JsonResponse({ "error": "Lecture ID is required" }, status=400)
        
        lecture = Lecture.objects.get(pk=lecture_id)
        students = lecture.students.all()
        students_data = []
        for student in students:
            students_data.append({
                "student_id": student.pk,
                "student_name": student.first_name + ' ' + student.last_name,
                "student_username": student.username,
            })
        return JsonResponse({ "students": students_data }, status=200)
    return JsonResponse({ "error": "Invalid request method" }, status=400)



# Endpoint to mark attendance of a student in a lecture - by creating a new HeldLecture object
# Takes a list of student usernames in the request body and a lecture_id, then creates
# a HeldLecture object and puts the students in it in held_lecture.students, and assigns the
# lecture to held_lecture. Then saves the held_lecture object.
"""
Input:
{
    "lecture_id": 1,
    "students": ["student1", "student2", "student3"]
}
"""

@csrf_exempt
@token_required
def mark_attendance(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)

        lecture_id = request.POST.get('lecture_id', '').strip()
        students = request.POST.getlist('students[]')

        if not lecture_id or not students:
            return JsonResponse({ "error": "Lecture ID and students list are required" }, status=400)
        
        lecture = Lecture.objects.get(pk=lecture_id)
        held_lecture = HeldLecture.objects.create(lecture=lecture)
        held_lecture.save()

        for student_username in students:
            student = User.objects.get(username=student_username)
            held_lecture.students.add(student)
        
        return JsonResponse({ "message": "Attendance marked successfully" }, status=201)
    return JsonResponse({ "error": "Invalid request method" }, status=400)