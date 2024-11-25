
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