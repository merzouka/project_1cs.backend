from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HaajSerializer
from authentication.models import utilisateur  

from rest_framework.permissions import IsAuthenticated

class DrawRegistrationView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        user_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'gender': request.user.gender,
            'city': request.user.city,
            'province': request.user.province,
            'dateOfBirth': request.user.dateOfBirth
        }
        serializer = HaajSerializer(data=user_data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        utilisateur_instance = utilisateur.objects.get(emailUtilisateur=request.user.email)
        serializer = HaajSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(utilisateur=utilisateur_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
