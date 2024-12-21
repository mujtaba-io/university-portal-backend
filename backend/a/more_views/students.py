from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.jwt_utils import *
import json
from ..models import *


# Student related views



@csrf_exempt
@token_required
def student_get(request):
    if request.method == 'GET':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if user.student:
            json_data = {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone,
                "admission_time": user.student.admission_time.strftime('%d-%m-%Y'),
                "roll_number": user.student.roll_number,
                "program": user.student.program,
                "cgpa": user.student.cgpa,
                "is_graduated": user.student.is_graduated,
                "is_dropout": user.student.is_dropout,

                "father_name": user.student.father_name,
                "father_occupation": user.student.father_occupation,
                "guardian_name": user.student.guardian_name,
                "guardian_occupation": user.student.guardian_occupation,
                "date_of_birth": user.student.date_of_birth.strftime('%d-%m-%Y'),
                "nic": user.student.nic,
                "blood_group": user.student.blood_group,
            }
            return JsonResponse(json_data, status=200)
        return JsonResponse({"error": "Student not found"}, status=404)
    
    return JsonResponse({"error": "Invalid request"}, status=400)





# Filter the logged in user's data (if it is a student) and return it
@csrf_exempt
@token_required
def student_time_table(request):
    if request.method == 'GET':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if user.student:
            # Get the lectures of the student, ignoring the makeup lectures
            lectures = user.student.lectures.all() # filter(is_makeup=False)
            lectures_data = []
            for lecture in lectures:
                lectures_data.append({
                    "course_name": lecture.course.name,
                    "course_code": lecture.course.code,
                    "teacher_name": lecture.teacher.first_name + ' ' + lecture.teacher.last_name,
                    "day": lecture.day,
                    "room": lecture.room.name,
                    "start_time": lecture.start_time.strftime('%H:%M'),
                    "end_time": lecture.end_time.strftime('%H:%M'),
                })
            return JsonResponse({ "timetable": lectures_data }, status=200)
        return JsonResponse({"error": "Student not found"}, status=404)
    
    return JsonResponse({"error": "Invalid request"}, status=400)


def student_makeup_lectures(request):
    if request.method == 'GET':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        if user.student:
            # Get the lectures of the student which are makeup & whose end time has not passed
            lectures = user.student.lectures.filter(is_makeup=True, end_time__gte=datetime.now().time())
            lectures_data = []
            for lecture in lectures:
                lectures_data.append({
                    "course_name": lecture.course.name,
                    "course_code": lecture.course.code,
                    "teacher_name": lecture.teacher.first_name + ' ' + lecture.teacher.last_name,
                    "day": lecture.day,
                    "room": lecture.room.name,
                    "start_time": lecture.start_time.strftime('%H:%M'),
                    "end_time": lecture.end_time.strftime('%H:%M'),
                })
            return JsonResponse({ "makeup_lectures": lectures_data }, status=200)
        return JsonResponse({"error": "Student not found"}, status=404)
    
    return JsonResponse({"error": "Invalid request"}, status=400)




""" @old implementation comment
Loop over all the held lectures,
if the lecture belonging to the held lecture is in the student's lectures,
then mark the attendance of the student in that lecture as present or absent
"""
@csrf_exempt
@token_required
def student_attendance(request):
    if request.method == 'GET':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)
        
        if user.student:
            attendance_data = []

            # Get all student's courses
            lectures = user.student.lectures.all() # To get lecture.course
            course_data = []
             # For each course, get all the held lectures
            for lecture in lectures:
                held_lectures = HeldLecture.objects.filter(lecture__course=lecture.course)
                held_lectures_absents = []
                for held_lecture in held_lectures:
                    if user.student in held_lecture.students.all():
                        continue
                    else:
                        held_lectures_absents.append({
                            "absent_date": held_lecture.created_at.strftime('%d-%m-%Y'),
                        })
                course_data.append({
                    "course_name": lecture.course.name,
                    "course_code": lecture.course.code,
                    "absents": held_lectures_absents,
                })
            attendance_data.append({
                "username": user.username,
                "attendance": course_data,
            })
            return JsonResponse({ "attendance": attendance_data }, status=200)
        return JsonResponse({"error": "Student not found"}, status=404)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

