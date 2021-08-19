from fastapi import APIRouter, Response
import base64
import random
import json
import requests
from src.config.configEnableX import ENABLEX_API_URL,ENABLEX_APP_ID,ENABLEX_APP_KEY
import http
room = APIRouter()



authbasic = 'Basic '
authbasicconv = base64.b64encode(
    (ENABLEX_APP_ID + ':' + ENABLEX_APP_KEY).encode("utf-8"))
auth = (authbasic + authbasicconv.decode())

headers = {"Content-Type": "application/json",
           'Authorization': 'Basic %s' % authbasicconv.decode()}
random_name = str(random.randint(100000, 999999))
payload = {
    'name': 'Sample Room: ' + random_name,
    'owner_ref': random_name,
    'settings': {
        'description': '',
        'quality': 'SD',
        'mode': 'group',
        'participants': '2',
        'duration': '60',
        'scheduled': False,
        'auto_recording': False,
        'active_talker': True,
        'wait_moderator': False,
        'adhoc': False,
    },
    'sip': {
        'enabled': False,
    }
}
encode_payload = json.JSONEncoder().encode(payload)



@room.get('/room')
def get_room(request, roomId):
    
    response = requests.get(ENABLEX_API_URL + '/rooms/' + str(roomId),
                            headers=headers)
    return Response(response.text)

@room.post('/room')
def create_room(request):
    response = requests.post(ENABLEX_API_URL + '/rooms',
                             headers=headers, json=payload)
    return Response(response.text)

def create_token(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        name = body['user_ref']
        role = body['role']
        roomId = body['roomId']
        user_ref = body['user_ref']
    else:
        return Response("Requested method is not allowed.")

    if roomId == '' or role == '' or user_ref == '':
        error = {'error': True}
        error['desc'] = "JSON keys missing: name, role or roomId"
        return Response(str(error))

    token = {
        "name": name,
        "role": role,
        "user_ref": user_ref
    }
    response = requests.post(ENABLEX_API_URL + '/rooms/' + roomId + '/tokens',
                             headers=headers, json=token)
    return Response(response)