from random import randint, random
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect

from authentication.serializers import UserSerializer
from .models import PasswordReset, User
from rest_framework. response import Response

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from django.contrib.auth import logout, login as authLogin
from django.urls import reverse
from .models import User

@api_view(["POST"])
@parser_classes([JSONParser])
def send_verification_email(request):
    email = request.data["email"]
    # email attached to account
    try:
        user: User = User.objects.get(email=email)
    except:
        return Response(JSONRenderer().render({ "message": "invalid address" }), 400)

    code = randint(0, 9999)
    try:
        send_mail(
            "Email de confirmation",
            f"Bienvenue sur le site Web El Hajj,\n votre code de confirmation est {code}",
            "celeq.elhajj@gmail.com",
            [email]
        )
        user.code = f"{code}"
        user.save()
        return Response(JSONRenderer().render({ "message": "email sent" }), 200)
    except:
        return Response(JSONRenderer().render({ "message": "invalid address" }), 400)

@api_view(["POST"])
@parser_classes([JSONParser])
def verify_email(request):
    email = request.data["email"]
    code = request.data["code"]

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
    try:
        hello = ""
    except:
        return Response(JSONRenderer().render({ "message": "duplicate email" }), 400)
    return Response(JSONRenderer().render(UserSerializer(user).data), status=200)


@api_view(["POST"])
@parser_classes([JSONParser])
def send_reset_password_email(request):
    email = request.data["email"]
    try:
        user: User = User.objects.get(email=email)
    except:
        return Response(JSONRenderer().render({ "message": "invalid address" }), 400)

    reset = PasswordReset()
    reset.save()
    reset.user = user
    reset.save()
    try:
        hello = ""
    except:
        return Response(JSONRenderer().render({ "message": "failed to send email" }), 400)
    id = reset._get_pk_val()
    link = f"http://localhost:3000/reset-password?id={id}&email={email}"
    try:
        send_mail(
            "Email de confirmation",
            f"Votre demande de réinitialisation de mot de passe a été approuvée. Veuillez suivre le lien\n {link}\n pour réinitialiser votre mot de passe.",
            "celeq.elhajj@gmail.com",
            [email]
        )
        return Response(JSONRenderer().render({ "message": "email sent" }), 200)
    except:
        return Response(JSONRenderer().render({ "message": "invalid address" }), 400)

@api_view(["PATCH"])
@parser_classes([JSONParser])
def reset_password(request):
    email = request.data["email"]
    reset_id = int(request.data["id"])
    new_password = request.data["newPassword"]
    try:
        reset: PasswordReset = PasswordReset.objects.get(pk=reset_id)
        user: User = User.objects.get(email=email)
        if user._get_pk_val() != reset.user._get_pk_val():
            return Response(JSONRenderer().render({ "message": "failed to reset password" }), 400)
        if user.check_password(new_password):
            return Response(JSONRenderer().render({ "message": "duplicate password" }), 409)
        user.set_password(new_password)
        user.save()
        reset.delete()
        return Response(JSONRenderer().render({ "message": "reset successful" }), 200)
    except:
        return Response(JSONRenderer().render({ "message": "failed to reset password" }), 400)


@api_view(['POST'])
@parser_classes([JSONParser])
def login(request):
    email = request.data["email"]
    password = request.data["password"]
    if not email or not password:
        return Response(JSONRenderer().render({ "message": "invalid credentials" }), 400)
    try:
        user: User = User.objects.get(email=email)
        if not user.check_password(password):
            return Response(JSONRenderer().render({ "message": "invalid credentials" }), 400)
        authLogin(request, user)
        return Response(JSONRenderer().render(UserSerializer(user).data), 200)
    except:
        return Response(JSONRenderer().render({ "message": "invalid credentials" }), 400)

def logout_user(request):
    logout(request)
    return redirect(reverse('login'))


@api_view(['GET'])
@parser_classes([JSONParser])
def default(request):
    try:
        send_mail(
            "Welcome",
            "How are you doing",
            "celeq.elhajj@gmail.com",
            ["marzoukayouness@gmail.com"]
        )
        return Response(JSONRenderer().render({ "message": "email sent successfully" }))
    except:
        return Response(JSONRenderer().render({ "message": "failed to send email" }), 400)
