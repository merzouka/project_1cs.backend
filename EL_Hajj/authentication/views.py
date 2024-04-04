from random import randint, random
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect

from authentication.serializers import UtilisateurSerializer,CustomUserSerializer
from .models import PasswordReset, CustomUser,utilisateur
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from django.contrib.auth import logout, login ,get_user_model,authenticate
from django.urls import reverse 
from django.views.decorators.csrf import csrf_exempt


@api_view(["POST"])
@parser_classes([JSONParser])
def send_verification_email(request):
    email = request.data["email"]
    # email attached to account
    try:
        user: CustomUser = CustomUser.objects.get(email=email)
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
    
    CustomUser = get_user_model()
    
    try:
        user = CustomUser.objects.get(email=email,code=code)
    except CustomUser.DoesNotExist:
        return Response(JSONRenderer().render({ "message": "invalid address or code" }), 400)
    user.is_email_verified = True 
    user.save()
    return Response(JSONRenderer().render({ "message": "Email verified" }), 200)
    
@csrf_exempt    
@api_view(['POST'])
@parser_classes([JSONParser])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)


    try:
        user = CustomUser.objects.create_user(email=email, password=password)
          # Assuming id_role is a list of role IDs
        user.save()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, 200)
    except Exception as e:
        return Response(JSONRenderer().render({ "message": "error" }), 400)
    


@api_view(['POST'])
@parser_classes([JSONParser])
def registerUtilisateur(request):
    serializer = UtilisateurSerializer(data=request.data)
    if serializer.is_valid():
        utilisateur = serializer.save()
        
        return Response(serializer.data,200)
    return Response(serializer.errors,400)


@api_view(["POST"])
@parser_classes([JSONParser])
def send_reset_password_email(request):
    email = request.data["email"]
    try:
        user: CustomUser = CustomUser.objects.get(email=email)
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
        user: CustomUser = CustomUser.objects.get(email=email)
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
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email and password:
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'},status=200)
        else:
            return Response({'error': 'Invalid email or password'}, status=401)
    else:
        return Response({'error': 'Email and password are required'}, status=400)


def logout_user(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"})


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
    
    

        
        
