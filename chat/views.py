from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
from decouple import config
def lobby(request):
    return render(request, 'lobby.html')

def room(request):
    return render(request, 'room.html', )

def getAGORA_APP_ID(request):
    appId = config('AGORA_APP_ID')
    return JsonResponse({'appId': appId}, safe=False)
            
def getToken(request):
    appId = config('AGORA_APP_ID')
    appCertificate = config('AGORA_APP_CERTIFICATE')
    channelName = request.GET.get('room')
    UID = random.randint(111 ,9999)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, UID, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'UID': UID}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room']
    )
    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    room = request.GET.get('room')
    uid = request.GET.get('UID')
    member = RoomMember.objects.get(room_name=room, uid=uid)
    name = member.name
    return JsonResponse({'name':name}, safe=False)

@csrf_exempt
def deleteMember(request):
    try:
        data = json.loads(request.body)
        member = RoomMember.objects.get(room_name=data['room'], name=data['name'] )
        member.delete()
        return JsonResponse({'status': 'ok'}, safe=False)
    except RoomMember.DoesNotExist:
        print('RoomMember not found')
        return JsonResponse({'status': 'error', 'message': 'RoomMember not found'}, safe=False)
    except json.JSONDecodeError:
        print('Invalid JSON')
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, safe=False)