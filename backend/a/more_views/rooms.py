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

        blocks = Block.objects.all()
        blocks_data = []

        for block in blocks:
            rooms = Room.objects.filter(block=block,is_lab=True)
            rooms_data = []
            for room in rooms:
                pcs = PC.objects.filter(room=room)
                pcs_data = []
                for pc in pcs:
                    pcs_data.append({
                        "pc_name": str(pc.pk),
                        "is_available": not pc.is_reserved('08:30-10:00')
                    })
                rooms_data.append({
                    "room_name": room.name,
                    "pcs": pcs_data,
                })
            blocks_data.append({
                "block_name": block.name,
                "rooms": rooms_data,
            })

        return JsonResponse(
            {
                "blocks": blocks_data,
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

        pc_name = request.POST['pc_name']
        time_slot = request.POST['time_slot']

        pc = PC.objects.get(pk=pc_name)

        # Check if the PC is available (not reserved at the given time)
        if pc.is_reserved(time_slot):
            return JsonResponse(
                {
                    "error": "PC is already reserved at the given time",
                },
                status=400
            )

        reservation = PCReservation(pc=pc, slot=time_slot)
        reservation.save()

        return JsonResponse(
            {
                "message": "PC reservation request sent to admin!",
            },
            status=200
        )
    return JsonResponse({"error": "Invalid request"}, status=400)

"""
Request:
POST at domain.com/api/rooms/book/
{
    "pc_id": 1,
    "time_slot": "08:30-10:00"
}
"""