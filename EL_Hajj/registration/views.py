from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HaajSerializer
from authentication.models import utilisateur 
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def registration(request):
    authenticated_user = request.user  
    if request.method == 'GET':
        utilisateur_data = {
            'emailUtilisateur': authenticated_user.email,
            'first_name': authenticated_user.first_name,
            'last_name': authenticated_user.last_name,
            'dateOfBirth': authenticated_user.date_of_birth,
            'city' : authenticated_user.city,
            'gender' : authenticated_user.gender
        }
        haaj_serializer = HaajSerializer(data=utilisateur_data)
        return Response(haaj_serializer.data)
    
    elif request.method == 'POST':
        haaj_serializer = HaajSerializer(data=request.data, context={'request': request})
        if haaj_serializer.is_valid():
            haaj_instance = haaj_serializer.save(user=authenticated_user)
            return Response(HaajSerializer(haaj_instance).data)
        return Response(haaj_serializer.errors, status=400)