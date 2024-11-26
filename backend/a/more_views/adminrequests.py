
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.jwt_utils import *
import json
from ..models import *


# PC reservation requests
@csrf_exempt
@token_required
def get_pc_requests(request):
    if request.method == 'GET':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)

        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can view PC reservation requests" }, status=403)

        rooms = Room.objects.filter(is_lab=True)
        rooms_data = []
        for room in rooms:
            pcs = PC.objects.filter(room=room)
            pcs_data = []
            for pc in pcs:
                pc_reservations = PCReservation.objects.filter(pc=pc)
                pc_reservations_data = []
                for pc_reservation in pc_reservations:
                    pc_reservations_data.append({
                        "pc_name": pc_reservation.pc.pk,
                        "user": pc_reservation.user.username,
                        "slot": pc_reservation.slot,
                        "is_approved": pc_reservation.is_approved,
                        "created_at": pc_reservation.created_at.strftime('%d-%m-%Y %H:%M:%S'),
                    })
                pcs_data.append({
                    "pc_name": pc.pk,
                    "reservations": pc_reservations_data,
                })
            rooms_data.append({
                "room_name": room.name,
                "pcs": pcs_data,
            })

        return JsonResponse(
            {
                "rooms": rooms_data,
            },
            status=200
        )
    return JsonResponse({"error": "Invalid request"}, status=400)



# Accept PC reservation request
@csrf_exempt
@token_required
def accept_pc_request(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)

        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can accept PC reservation requests" }, status=403)

        pc_name = request.POST.get('pc_name', '').strip()
        username = request.POST.get('username', '').strip()
        slot = request.POST.get('slot', '').strip()

        if not pc_name or not username or not slot:
            return JsonResponse({ "error": "PC name, user name and slot are required" }, status=400)

        pc = PC.objects.get(pk=pc_name)
        user = User.objects.get(username=username)

        pc_reservation = PCReservation.objects.get(pc=pc, user=user, slot=slot)
        pc_reservation.is_approved = True
        pc_reservation.save()

        return JsonResponse(
            {
                "message": "PC reservation request accepted",
            },
            status=200
        )
    return JsonResponse({"error": "Invalid request"}, status=400)



# Reject PC reservation request
@csrf_exempt
@token_required
def reject_pc_request(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)

        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can reject PC reservation requests" }, status=403)

        pc_name = request.POST.get('pc_name', '').strip()
        username = request.POST.get('username', '').strip()
        slot = request.POST.get('slot', '').strip()

        if not pc_name or not username or not slot:
            return JsonResponse({ "error": "PC name, user name and slot are required" }, status=400)

        pc = PC.objects.get(pk=pc_name)
        user = User.objects.get(username=username)

        pc_reservation = PCReservation.objects.get(pc=pc, user=user, slot=slot)
        pc_reservation.delete()

        return JsonResponse(
            {
                "message": "PC reservation request rejected",
            },
            status=200
        )
    return JsonResponse({"error": "Invalid request"}, status=400)









# Endpoints for admin requests for makeup classes

# Get makeup class requests
@csrf_exempt
@token_required
def get_makeup_lecture_requests(request):
    if request.method == 'GET':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)

        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can view makeup class requests" }, status=403)

        makeup_lectures = Lecture.objects.filter(is_makeup=True)
        makeup_lectures_data = []
        for makeup_lecture in makeup_lectures:
            makeup_lectures_data.append({
                "lecture_id": makeup_lecture.pk,
                "course": makeup_lecture.course.name,
                "teacher": makeup_lecture.teacher.username,
                "day": makeup_lecture.day,
                "room": makeup_lecture.room.name,
                "start_time": makeup_lecture.start_time.strftime('%H:%M'),
                "end_time": makeup_lecture.end_time.strftime('%H:%M'),
                "is_makeup_approved": makeup_lecture.is_makeup_approved,
                "created_at": makeup_lecture.created_at.strftime('%d-%m-%Y %H:%M:%S'),
            })

        return JsonResponse(
            {
                "makeup_lectures": makeup_lectures_data,
            },
            status=200
        )
    return JsonResponse({"error": "Invalid request"}, status=400)




# Accept makeup class request
@csrf_exempt
@token_required
def accept_makeup_lecture_request(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)

        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can accept makeup class requests" }, status=403)

        lecture_id = request.POST.get('lecture_id', '').strip()

        if not lecture_id:
            return JsonResponse({ "error": "Lecture ID is required" }, status=400)

        lecture = Lecture.objects.get(pk=lecture_id)
        lecture.is_makeup_approved = True
        lecture.save()

        return JsonResponse(
            {
                "message": "Makeup class request accepted",
            },
            status=200
        )
    return JsonResponse({"error": "Invalid request"}, status=400)



# Reject makeup class request
@csrf_exempt
@token_required
def reject_makeup_lecture_request(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)

        if not user.is_superuser or not user.is_staff:
            return JsonResponse({ "error": "Only admin can reject makeup class requests" }, status=403)

        lecture_id = request.POST.get('lecture_id', '').strip()

        if not lecture_id:
            return JsonResponse({ "error": "Lecture ID is required" }, status=400)

        lecture = Lecture.objects.get(pk=lecture_id)
        lecture.delete()

        return JsonResponse(
            {
                "message": "Makeup class request rejected",
            },
            status=200
        )
    return JsonResponse({"error": "Invalid request"}, status=400)