from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HaajSerializer , HaajaSerializer
from authentication.models import utilisateur 
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def registration(request):
    authenticated_user = request.user  
    if request.method == 'GET':
        authenticated_user = request.user
        utilisateur_instance = get_object_or_404(utilisateur, emailUtilisateur=authenticated_user)
        utilisateur_data = {
            'emailUtilisateur': utilisateur_instance.emailUtilisateur.email,
            'first_name': utilisateur_instance.first_name,
            'last_name': utilisateur_instance.last_name,
            'dateOfBirth': utilisateur_instance.dateOfBirth,
            'city' : utilisateur_instance.city,
            'gender' : utilisateur_instance.gender
        }
        return JsonResponse(utilisateur_data)
    
    elif request.method == 'POST':
        authenticated_user = request.user
        utilisateur_instance = authenticated_user.utilisateur
        serializer_data = request.data.copy() 
        
        if utilisateur_instance.gender == 'F':  
            haaja_serializer = HaajaSerializer(data=serializer_data, context={'request': request})
            if haaja_serializer.is_valid():
                haaja_instance = haaja_serializer.save()
                return Response("Success", status=status.HTTP_201_CREATED)
            return Response(haaja_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            haaj_serializer = HaajSerializer(data=serializer_data, context={'request': request})
            if haaj_serializer.is_valid():
                haaj_instance = haaj_serializer.save()
                return Response("Success", status=status.HTTP_201_CREATED)
            return Response(haaj_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    