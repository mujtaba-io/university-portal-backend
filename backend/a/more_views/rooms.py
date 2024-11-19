from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.jwt_utils import *
import json
from ..models import *



@csrf_exempt
@token_required
def get_pcs(request):
    if request.method == 'GET':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)

        rooms = Room.objects.all()
        rooms_data = []

        for room in rooms:
            if room.is_lab:
                pcs = PC.objects.filter(room=room)
                pcs_data = []
                for pc in pcs:
                    pcs_data.append({
                        "pc_name": str(pc.pk),
                        "is_available": not pc.is_reserved(datetime.datetime.now().time())
                    })
                rooms_data.append({
                    "room_name": room.name,
                    "pcs": pcs_data,
                })
        return JsonResponse(
            {
                "pcs": rooms_data,
            },
            status=200
        )
    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
@token_required
def book_pc(request):
    if request.method == 'POST':
        token = request.headers.get('token')
        username = decode_jwt_token(token)
        user = User.objects.get(username=username)

        pc_id = request.POST['pc_id']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        pc = PC.objects.get(pk=pc_id)

        # Check if the PC is available (not reserved at the given time)
        if pc.is_reserved(start_time) or pc.is_reserved(end_time):
            return JsonResponse(
                {
                    "error": "PC is already reserved at the given time",
                },
                status=400
            )

        reservation = PCReservation(pc=pc, start_time=start_time, end_time=end_time)
        reservation.save()

        return JsonResponse(
            {
                "message": "PC reserved",
            },
            status=200
        )
    return JsonResponse({"error": "Invalid request"}, status=400)