from django.shortcuts import redirect

from authentication.serializers import UserSerializer
from .models import User
from rest_framework. response import Response

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from django.contrib.auth import login, logout
from django.urls import reverse
from .models import User
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_verification_email(user, req):
    pass

@api_view(['POST'])
@parser_classes([JSONParser])
def register(request):
    request.data["gender"] = "M" if request.data["gender"] == "male" else "F"
    request.data["first_name"] = request.data["firstName"]
    request.data["last_name"] = request.data["lastName"]
    del request.data["firstName"]
    del request.data["lastName"]

    user = User(**request.data)
    user.set_password(request.data["password"])
    print(UserSerializer(user))
    user.save()
    return Response(JSONRenderer().render(UserSerializer(user).data), status=200)


def send_reset_password_email(request):
    pass

def reset_password(request):
    pass


@api_view(['POST'])
@parser_classes([JSONParser])
def login_user(request):
    try:
        user = User.objects.get(email=request.data.email)
        print(user)
        if not user.check_password(request.data.password, user.password):
            return Response(JSONRenderer().render({ "message": "invalid credentials" }), status=400)
        login(request, user)
        return Response(JSONRenderer().render(UserSerializer(user).data), status=200)
    except: 
        return Response(JSONRenderer().render({ "message": "invalid credentials" }), status=400);

def logout_user(request):
    logout(request)
    return redirect(reverse('login'))


@api_view(['GET'])
@parser_classes([JSONParser])
def default(request):
    return Response(JSONRenderer().render({ "message": "hello world" }))
